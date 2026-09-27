#!/usr/bin/env python3
"""Remap NDT7 coordinate aggregates onto the supplied geoBoundaries ADM1 layers.

The clean parquet files are read-only inputs. Coordinates are assigned to ADM1
polygons once per unique location, then quarterly/network summaries are rebuilt
using those assignments. Output files are written under the analysis project.
"""

from __future__ import annotations

import argparse
import csv
import gc
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

import duckdb
import geopandas as gpd
import pandas as pd
from shapely.geometry import mapping


COUNTRIES = {
    "cambodia": ("Cambodia", "kh", "KHM"),
    "indonesia": ("Indonesia", "id", "IDN"),
    "laos": ("Laos", "la", "LAO"),
    "malaysia": ("Malaysia", "my", "MYS"),
    "myanmar": ("Myanmar", "mm", "MMR"),
    "philippines": ("Philippines", "ph", "PHL"),
    "singapore": ("Singapore", "sg", "SGP"),
    "thailand": ("Thailand", "th", "THA"),
    "vietnam": ("Vietnam", "vn", "VNM"),
}

# Source labels used by existing cleaning/export workflows.
NAME_ALIASES = {
    "indonesia": {
        "bangkabelitung": "Bangka-Belitung Islands",
        "jakarta": "Jakarta Special Capital Region",
        "yogyakarta": "Special Region of Yogyakarta",
    },
    "myanmar": {
        "sagaing": "Saigang",
        "tanintharyi": "Tanitharyi",
        # Existing Myanmar preparation convention: no separate ADM1 polygon.
        "naypyitaw": "Mandalay",
    },
}

NETWORK_TYPES = ("broadband", "cellular", "hosting")


def normalize(value: Any) -> str:
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def canonical_source_name(country: str, value: Any) -> str:
    raw = str(value or "").strip()
    alias = NAME_ALIASES.get(country, {}).get(normalize(raw))
    return alias or raw


def feature_name(properties: dict[str, Any]) -> str:
    return str(properties.get("shapeName") or properties.get("name") or "").strip()


def load_boundaries(path: Path, iso3: str):
    layer = gpd.read_file(path)
    if layer.crs is None:
        layer = layer.set_crs("EPSG:4326")
    layer = layer.to_crs("EPSG:4326")
    layer["adm1_name"] = layer.apply(lambda row: feature_name(row.to_dict()), axis=1)
    layer["country_iso3"] = iso3
    layer["geoBoundary_shapeID"] = layer.get("shapeID", pd.Series(index=layer.index, dtype="object")).fillna("").astype(str)
    layer["map_join_key"] = layer.apply(
        lambda row: row["geoBoundary_shapeID"] or f"{iso3}-ADM1:{normalize(row['adm1_name'])}", axis=1
    )
    layer["map_id_origin"] = layer["geoBoundary_shapeID"].map(
        lambda value: "geoBoundaries shapeID" if value else "derived ISO3 + normalized name"
    )
    if layer["adm1_name"].map(normalize).duplicated().any():
        duplicated = layer.loc[layer["adm1_name"].map(normalize).duplicated(), "adm1_name"].tolist()
        raise ValueError(f"Ambiguous GeoBoundary names in {path.name}: {duplicated}")
    layer["_area_m2"] = layer.to_crs("EPSG:6933").geometry.area.to_numpy()
    return layer


def assign_coordinates(layer, coordinates: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Assign each distinct finite lon/lat point to exactly one ADM1 polygon."""
    valid = coordinates.dropna(subset=["latitude", "longitude"]).drop_duplicates().copy()
    valid = valid.reset_index(drop=True)
    valid["coord_id"] = range(len(valid))
    points = gpd.GeoDataFrame(
        valid[["coord_id", "latitude", "longitude"]],
        geometry=gpd.points_from_xy(valid["longitude"], valid["latitude"]),
        crs="EPSG:4326",
    )
    polygons = layer[["adm1_name", "map_join_key", "_area_m2", "geometry"]]
    hit = gpd.sjoin(points, polygons, how="left", predicate="within")
    hit = hit.sort_values(["coord_id", "_area_m2"], na_position="last").drop_duplicates("coord_id")
    hit["assignment_method"] = hit["index_right"].notna().map({True: "within", False: "nearest"})
    missing = hit[hit["index_right"].isna()]
    if len(missing):
        nearest = gpd.sjoin_nearest(
            points.loc[missing.index].to_crs("EPSG:6933"),
            polygons[["adm1_name", "map_join_key", "geometry"]].to_crs("EPSG:6933"),
            how="left",
            distance_col="nearest_distance_m",
        )
        nearest = nearest.sort_values(["coord_id", "nearest_distance_m"]).drop_duplicates("coord_id")
        nearest_by_id = nearest.set_index("coord_id")
        for idx in missing.index:
            coord_id = int(hit.loc[idx, "coord_id"])
            hit.loc[idx, "adm1_name"] = nearest_by_id.loc[coord_id, "adm1_name"]
            hit.loc[idx, "map_join_key"] = nearest_by_id.loc[coord_id, "map_join_key"]
    result = hit[["coord_id", "latitude", "longitude", "adm1_name", "map_join_key", "assignment_method"]].copy()
    result["latitude"] = result["latitude"].astype(float)
    result["longitude"] = result["longitude"].astype(float)
    counts = {
        "unique_coordinates": int(len(result)),
        "within_coordinates": int((result["assignment_method"] == "within").sum()),
        "nearest_fallback_coordinates": int((result["assignment_method"] == "nearest").sum()),
    }
    return result, counts


def quote_sql_path(path: Path) -> str:
    return path.resolve().as_posix().replace("'", "''")


def extract_coordinate_metrics(con, parquet_path: Path, is_ph: bool) -> pd.DataFrame:
    p = quote_sql_path(parquet_path)
    area = "COALESCE(region, province)" if is_ph else "province"
    region = "region" if is_ph else "NULL::VARCHAR AS region"
    # Retain zero/invalid throughput rows in coordinate coverage, but only positive
    # throughput observations contribute to the exported speed summaries.
    sql = f"""
        SELECT
            CAST(latitude AS DOUBLE) AS latitude,
            CAST(longitude AS DOUBLE) AS longitude,
            province,
            {region},
            CAST({area} AS VARCHAR) AS old_area,
            CAST(year AS INTEGER) AS year,
            CAST(CEIL(month / 3.0) AS INTEGER) AS quarter_num,
            network_type,
            COUNT(*) FILTER (WHERE type='download' AND mean_throughput_mbps > 0) AS download_tests,
            SUM(mean_throughput_mbps) FILTER (WHERE type='download' AND mean_throughput_mbps > 0) AS download_sum_mbps,
            COUNT(*) FILTER (WHERE type='upload' AND mean_throughput_mbps > 0) AS upload_tests,
            SUM(mean_throughput_mbps) FILTER (WHERE type='upload' AND mean_throughput_mbps > 0) AS upload_sum_mbps,
            COUNT(*) FILTER (WHERE type='download' AND min_rtt IS NOT NULL AND min_rtt < 2000) AS latency_tests,
            SUM(min_rtt) FILTER (WHERE type='download' AND min_rtt IS NOT NULL AND min_rtt < 2000) AS latency_sum_ms
        FROM read_parquet('{p}')
        WHERE network_type IN ('broadband','cellular','hosting')
        GROUP BY latitude, longitude, province, region, old_area, year, quarter_num, network_type
    """
    return con.execute(sql).fetchdf()


def build_country(country: str, con, data_root: Path, output_temp: Path):
    display, short_code, iso3 = COUNTRIES[country]
    parquet = data_root / "ndt7" / short_code / f"mlab_{short_code}_clean.parquet"
    geojson = data_root / "geo" / f"{country}_provinces.geojson"
    if not parquet.exists():
        raise FileNotFoundError(f"Missing NDT7 cleaned parquet: {parquet}")
    if not geojson.exists():
        raise FileNotFoundError(f"Missing geoBoundaries ADM1 layer: {geojson}")

    layer = load_boundaries(geojson, iso3)
    raw = extract_coordinate_metrics(con, parquet, country == "philippines")
    coords = raw[["latitude", "longitude"]].dropna().drop_duplicates()
    assigned, assignment_counts = assign_coordinates(layer, coords)
    raw = raw.merge(assigned, on=["latitude", "longitude"], how="left", validate="many_to_one")

    # Establish the old-label to new-label crosswalk. Prefer an exact/explicit
    # name match; for transliteration differences, infer the counterpart from
    # the dominant spatial match for that old area, then count its outliers.
    feature_name_by_key = {normalize(n): n for n in layer["adm1_name"]}
    expected_by_old: dict[str, tuple[str, str]] = {}
    for old_area, old_rows in raw.groupby("old_area", dropna=False):
        if pd.isna(old_area):
            continue
        alias = canonical_source_name(country, old_area)
        direct = feature_name_by_key.get(normalize(alias))
        if direct:
            expected_by_old[str(old_area)] = (direct, "normalized name / explicit alias")
            continue
        spatial_rows = old_rows[old_rows["adm1_name"].notna()]
        counts = (
            spatial_rows.groupby("adm1_name", dropna=False)
            .agg(download_tests=("download_tests", "sum"), coordinate_groups=("latitude", "size"))
            .sort_values(["download_tests", "coordinate_groups"], ascending=False)
        )
        if not counts.empty and counts.index[0]:
            expected_by_old[str(old_area)] = (str(counts.index[0]), "dominant spatial match for transliteration/name variant")

    # When coordinates are absent, use a documented area-name or spatially
    # inferred crosswalk only if it identifies exactly one ADM1 feature.
    missing_location = raw["adm1_name"].isna()
    for index in raw.index[missing_location]:
        old_area = raw.at[index, "old_area"]
        expected = expected_by_old.get(str(old_area)) if pd.notna(old_area) else None
        if expected:
            match = layer[layer["adm1_name"] == expected[0]]
            if len(match) == 1:
                raw.at[index, "adm1_name"] = expected[0]
                raw.at[index, "map_join_key"] = match.iloc[0]["map_join_key"]
                raw.at[index, "assignment_method"] = "old_area_crosswalk_no_coordinates"

    unmapped = raw[raw["adm1_name"].isna() | raw["map_join_key"].isna()].copy()
    mapped_raw = raw.drop(index=unmapped.index).copy()

    mapped_raw["expected_geoBoundary_name"] = mapped_raw["old_area"].map(
        lambda value: expected_by_old.get(str(value), (None, "no previous area label"))[0] if pd.notna(value) else None
    )
    mapped_raw["old_to_boundary_method"] = mapped_raw["old_area"].map(
        lambda value: expected_by_old.get(str(value), (None, "no previous area label"))[1] if pd.notna(value) else "no previous area label"
    )
    mapped_raw["assignment_changed"] = mapped_raw.apply(
        lambda row: (
            normalize(row["expected_geoBoundary_name"]) != normalize(row["adm1_name"])
            if pd.notna(row["expected_geoBoundary_name"]) else False
        ),
        axis=1,
    )
    changes = (
        mapped_raw.groupby(["old_area", "expected_geoBoundary_name", "adm1_name", "assignment_changed"], dropna=False, as_index=False)
        .agg(download_tests=("download_tests", "sum"), upload_tests=("upload_tests", "sum"), coordinate_groups=("latitude", "size"))
    )
    changes.insert(0, "country", display)
    changes.insert(1, "country_iso3", iso3)

    # Aggregate coordinate contributions by their newly assigned GeoBoundary unit.
    group_cols = ["adm1_name", "map_join_key", "network_type", "year", "quarter_num"]
    summary = (
        mapped_raw.groupby(group_cols, dropna=False, as_index=False)
        .agg(
            download_tests=("download_tests", "sum"),
            download_sum_mbps=("download_sum_mbps", "sum"),
            upload_tests=("upload_tests", "sum"),
            upload_sum_mbps=("upload_sum_mbps", "sum"),
            latency_tests=("latency_tests", "sum"),
            latency_sum_ms=("latency_sum_ms", "sum"),
            n_coordinates=("longitude", "size"),
        )
    )
    summary["avg_d_mbps"] = summary["download_sum_mbps"] / summary["download_tests"].replace(0, pd.NA)
    summary["avg_u_mbps"] = summary["upload_sum_mbps"] / summary["upload_tests"].replace(0, pd.NA)
    summary["avg_lat_ms_wt"] = summary["latency_sum_ms"] / summary["latency_tests"].replace(0, pd.NA)
    summary["quarter"] = summary.apply(lambda r: f"{int(r.year)}-Q{int(r.quarter_num)}", axis=1)
    summary["is_reliable"] = summary["download_tests"].fillna(0) >= 100
    summary["country"] = display
    summary["country_iso3"] = iso3
    summary["geoBoundary_shapeID"] = summary["map_join_key"].map(
        dict(zip(layer["map_join_key"], layer["geoBoundary_shapeID"]))
    )
    summary["coordinate_mapping"] = "GeoBoundary point-in-polygon; nearest fallback when outside"
    summary = summary[
        [
            "country", "country_iso3", "adm1_name", "geoBoundary_shapeID", "map_join_key",
            "network_type", "quarter", "year", "quarter_num", "avg_d_mbps", "avg_u_mbps",
            "avg_lat_ms_wt", "download_tests", "upload_tests", "latency_tests",
            "n_coordinates", "is_reliable", "coordinate_mapping",
        ]
    ]

    # Crosswalk for the actual source area labels seen in the cleaned data.
    crosswalk = (
        mapped_raw.groupby(["old_area", "expected_geoBoundary_name", "old_to_boundary_method", "adm1_name", "map_join_key", "assignment_changed"], dropna=False, as_index=False)
        .agg(download_tests=("download_tests", "sum"), upload_tests=("upload_tests", "sum"), coordinate_groups=("latitude", "size"))
    )
    crosswalk.insert(0, "country", display)
    crosswalk.insert(1, "country_iso3", iso3)
    crosswalk["geoBoundary_shapeID"] = crosswalk["map_join_key"].map(
        dict(zip(layer["map_join_key"], layer["geoBoundary_shapeID"]))
    )
    crosswalk = crosswalk.rename(columns={
        "expected_geoBoundary_name": "crosswalk_geoBoundary_name",
        "old_to_boundary_method": "crosswalk_method",
    })
    crosswalk["mapping_method"] = crosswalk["assignment_changed"].map(
        {True: "coordinate reassigned to a different ADM1", False: "same ADM1 label after alias normalization"}
    )
    crosswalk.loc[crosswalk["crosswalk_method"] == "no previous area label", "mapping_method"] = "coordinate assigned; no old area label to compare"

    # Add all boundary polygons, including places with no tests, once per network type.
    geo_features: list[dict[str, Any]] = []
    summary_by_key_type = {}
    for (map_key, network_type), frame in summary.groupby(["map_join_key", "network_type"]):
        dl_tests = int(frame["download_tests"].fillna(0).sum())
        ul_tests = int(frame["upload_tests"].fillna(0).sum())
        lat_tests = int(frame["latency_tests"].fillna(0).sum())
        summary_by_key_type[(map_key, network_type)] = {
            "total_download_tests": dl_tests,
            "total_upload_tests": ul_tests,
            "n_quarters": int(frame["quarter"].nunique()),
            "avg_d_mbps": float((frame["avg_d_mbps"].fillna(0) * frame["download_tests"].fillna(0)).sum() / dl_tests) if dl_tests else None,
            "avg_u_mbps": float((frame["avg_u_mbps"].fillna(0) * frame["upload_tests"].fillna(0)).sum() / ul_tests) if ul_tests else None,
            "avg_lat_ms_wt": float((frame["avg_lat_ms_wt"].fillna(0) * frame["latency_tests"].fillna(0)).sum() / lat_tests) if lat_tests else None,
        }
    for _, boundary in layer.iterrows():
        props = boundary.drop(labels="geometry").to_dict()
        # Avoid serializing GeoPandas helper columns as data attributes.
        props.pop("_area_m2", None)
        map_key = props["map_join_key"]
        for network_type in NETWORK_TYPES:
            stats = summary_by_key_type.get((map_key, network_type))
            if not stats:
                stats = {
                    "total_download_tests": 0,
                    "total_upload_tests": 0,
                    "n_quarters": 0,
                    "avg_d_mbps": None,
                    "avg_u_mbps": None,
                    "avg_lat_ms_wt": None,
                }
            prefix = network_type
            props[f"{prefix}_download_tests"] = int(stats["total_download_tests"])
            props[f"{prefix}_upload_tests"] = int(stats["total_upload_tests"])
            props[f"{prefix}_quarters"] = int(stats["n_quarters"])
            props[f"{prefix}_avg_d_mbps"] = None if pd.isna(stats["avg_d_mbps"]) else float(stats["avg_d_mbps"])
            props[f"{prefix}_avg_u_mbps"] = None if pd.isna(stats["avg_u_mbps"]) else float(stats["avg_u_mbps"])
            props[f"{prefix}_avg_lat_ms_wt"] = None if pd.isna(stats["avg_lat_ms_wt"]) else float(stats["avg_lat_ms_wt"])
        geo_features.append(
            {
                "type": "Feature",
                "geometry": mapping(boundary.geometry),
                "properties": props,
            }
        )

    changed_download = int(changes.loc[changes["assignment_changed"], "download_tests"].sum())
    total_download = int(summary["download_tests"].sum())
    unmapped_download = int(unmapped["download_tests"].fillna(0).sum())
    unmapped_upload = int(unmapped["upload_tests"].fillna(0).sum())
    diagnostics = {
        "country": display,
        "country_iso3": iso3,
        "boundary_features": int(len(layer)),
        **assignment_counts,
        "coordinate_groups_with_metrics": int(len(raw)),
        "area_labels_before": int(raw["old_area"].nunique(dropna=True)),
        "area_labels_after": int(raw["adm1_name"].nunique()),
        "changed_assignment_download_tests": changed_download,
        "total_download_tests": total_download,
        "changed_assignment_percent": 100 * changed_download / total_download if total_download else 0,
        "unmatched_coordinate_groups": int(len(unmapped)),
        "unmapped_download_tests": unmapped_download,
        "unmapped_upload_tests": unmapped_upload,
        "source_download_tests": total_download + unmapped_download,
        "quarter_network_rows": int(len(summary)),
    }
    del raw, mapped_raw, coords, assigned
    gc.collect()
    return summary, crosswalk, changes, geo_features, diagnostics, unmapped


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=Path(r"E:\ndt7\data"))
    parser.add_argument("--output-root", type=Path, default=Path("data"))
    parser.add_argument("--memory-limit", default="8GB")
    parser.add_argument("--threads", type=int, default=8)
    args = parser.parse_args()

    output_exports = args.output_root / "exports"
    output_geo = args.output_root / "geo"
    temp_directory = args.output_root / ".tmp" / "duckdb-geoboundaries"
    output_exports.mkdir(parents=True, exist_ok=True)
    output_geo.mkdir(parents=True, exist_ok=True)
    temp_directory.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()
    con.execute(f"SET memory_limit='{args.memory_limit}'")
    con.execute(f"SET temp_directory='{temp_directory.resolve().as_posix()}'")
    con.execute(f"SET threads={int(args.threads)}")
    con.execute("SET preserve_insertion_order=false")

    all_summaries: list[pd.DataFrame] = []
    all_crosswalks: list[pd.DataFrame] = []
    all_changes: list[pd.DataFrame] = []
    all_features: list[dict[str, Any]] = []
    all_unmapped: list[pd.DataFrame] = []
    diagnostics: list[dict[str, Any]] = []
    for country in COUNTRIES:
        print(f"Mapping {COUNTRIES[country][0]}...")
        summary, crosswalk, changes, features, report, unmapped = build_country(country, con, args.data_root, temp_directory)
        all_summaries.append(summary)
        all_crosswalks.append(crosswalk)
        all_changes.append(changes)
        all_features.extend(features)
        if len(unmapped):
            all_unmapped.append(unmapped.assign(country=report["country"], country_iso3=report["country_iso3"]))
        diagnostics.append(report)
        print(
            f"  {report['boundary_features']} ADM1 polygons; "
            f"{report['changed_assignment_download_tests']:,}/{report['total_download_tests']:,} "
            f"download observations map to a different ADM1 label"
        )

    quarterly = pd.concat(all_summaries, ignore_index=True)
    quarterly_path = output_exports / "ndt7_geoboundaries_adm1_quarterly.csv"
    quarterly.to_csv(quarterly_path, index=False, encoding="utf-8-sig")

    crosswalk_df = pd.concat(all_crosswalks, ignore_index=True)
    crosswalk_path = output_exports / "ndt7_geoboundaries_adm1_crosswalk.csv"
    crosswalk_df.to_csv(crosswalk_path, index=False, encoding="utf-8-sig")

    changes_df = pd.concat(all_changes, ignore_index=True)
    changes_path = output_exports / "ndt7_geoboundaries_adm1_assignment_changes.csv"
    changes_df.to_csv(changes_path, index=False, encoding="utf-8-sig")

    unmapped_df = pd.concat(all_unmapped, ignore_index=True) if all_unmapped else pd.DataFrame()
    unmapped_path = output_exports / "ndt7_geoboundaries_unmapped_coordinate_groups.csv"
    unmapped_df.to_csv(unmapped_path, index=False, encoding="utf-8-sig")

    geojson_path = output_geo / "ndt7_geoboundaries_adm1_summary.geojson"
    feature_collection = {
        "type": "FeatureCollection",
        "name": "NDT7 remapped to geoBoundaries ADM1",
        "source": "Cleaned M-Lab NDT7 parquet files under E:/ndt7/data/ndt7 plus supplied E:/ndt7/data/geo GeoJSON boundaries",
        "method": "Unique coordinates were spatially joined to GeoBoundaries ADM1 polygons; quarterly metrics were rebuilt from the cleaned parquet records.",
        "metric_fields": "Per network_type, avg_d_mbps/avg_u_mbps/avg_lat_ms_wt are pooled test-weighted summaries over available quarters; see the quarterly CSV for full periods.",
        "features": all_features,
    }
    geojson_path.write_text(json.dumps(feature_collection, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # Compare current published country × area × quarter exports against the remapped
    # aggregates. The new GeoBoundary aggregates are already complete; this is a
    # diagnostic indicating whether downstream RQ notebooks need refreshing.
    comparisons: list[dict[str, Any]] = []
    data_exports = args.data_root / "exports"
    old_area_to_boundary: dict[tuple[str, str], str] = {}
    for item in crosswalk_df[["country_iso3", "old_area", "crosswalk_geoBoundary_name"]].drop_duplicates().itertuples(index=False):
        old_area_to_boundary[(item.country_iso3, normalize(item.old_area))] = item.crosswalk_geoBoundary_name
    for country, (display, _, iso3) in COUNTRIES.items():
        for network_type, prefix in (("broadband", ""), ("cellular", "mobile_")):
            old_path = data_exports / f"ndt7_{prefix}{country}_province_quarterly.csv"
            if not old_path.exists():
                continue
            with old_path.open("r", encoding="utf-8-sig", newline="") as handle:
                old_rows = list(csv.DictReader(handle))
            new_rows = quarterly[(quarterly.country_iso3 == iso3) & (quarterly.network_type == network_type)].copy()
            gb_names = {normalize(n): n for n in new_rows["adm1_name"].drop_duplicates()}
            old_groups: dict[tuple[str, str], dict[str, float]] = defaultdict(lambda: {"tests": 0.0, "dl_sum": 0.0, "ul_sum": 0.0, "ul_tests": 0.0, "lat_sum": 0.0, "lat_tests": 0.0})
            duplicate_keys: dict[tuple[str, str], int] = defaultdict(int)
            unmatched_old = 0
            for row in old_rows:
                old_area = row.get("province")
                candidate = canonical_source_name(country, old_area)
                gb_name = old_area_to_boundary.get((iso3, normalize(old_area))) or gb_names.get(normalize(candidate))
                if not gb_name:
                    unmatched_old += 1
                    continue
                key = (gb_name, row.get("quarter", ""))
                duplicate_keys[key] += 1
                tests = float(row.get("total_tests") or 0)
                old_groups[key]["tests"] += tests
                if row.get("avg_d_mbps") not in (None, ""):
                    old_groups[key]["dl_sum"] += float(row["avg_d_mbps"]) * tests
                if row.get("avg_u_mbps") not in (None, ""):
                    old_groups[key]["ul_sum"] += float(row["avg_u_mbps"]) * tests
                    old_groups[key]["ul_tests"] += tests
                if row.get("avg_lat_ms_wt") not in (None, ""):
                    old_groups[key]["lat_sum"] += float(row["avg_lat_ms_wt"]) * tests
                    old_groups[key]["lat_tests"] += tests

            new_groups = {
                (row.adm1_name, row.quarter): row
                for row in new_rows.itertuples(index=False)
            }
            keys = set(old_groups) | set(new_groups)
            changed_keys = 0
            changed_tests = 0.0
            max_abs_dl_delta = 0.0
            for key in keys:
                old = old_groups.get(key)
                new = new_groups.get(key)
                old_tests = old["tests"] if old else 0.0
                new_tests = float(new.download_tests or 0) if new else 0.0
                old_dl = old["dl_sum"] / old_tests if old and old_tests else None
                new_dl = float(new.avg_d_mbps) if new and pd.notna(new.avg_d_mbps) else None
                count_diff = abs(old_tests - new_tests) > 0.5
                speed_diff = (old_dl is None) != (new_dl is None) or (old_dl is not None and new_dl is not None and abs(old_dl - new_dl) > 1e-6)
                if count_diff or speed_diff:
                    changed_keys += 1
                    changed_tests += max(old_tests, new_tests)
                if old_dl is not None and new_dl is not None:
                    max_abs_dl_delta = max(max_abs_dl_delta, abs(old_dl - new_dl))
            comparisons.append(
                {
                    "country": display,
                    "network_type": network_type,
                    "old_export_rows": len(old_rows),
                    "old_duplicate_area_quarter_keys": sum(1 for n in duplicate_keys.values() if n > 1),
                    "unmatched_old_export_rows": unmatched_old,
                    "old_tests_sum": int(sum(v["tests"] for v in old_groups.values())),
                    "new_tests_sum": int(new_rows["download_tests"].sum()),
                    "different_area_quarter_keys": changed_keys,
                    "max_abs_download_mean_difference_mbps": max_abs_dl_delta,
                }
            )

    compare_path = output_exports / "ndt7_geoboundaries_adm1_existing_export_comparison.csv"
    pd.DataFrame(comparisons).to_csv(compare_path, index=False, encoding="utf-8-sig")

    report_path = output_exports / "ndt7_geoboundaries_adm1_mapping_check.md"
    lines = [
        "# NDT7 GeoBoundaries ADM1 remapping check",
        "",
        "The nine cleaned NDT7 parquet datasets were read without modification. Distinct coordinates were assigned to the supplied country ADM1 polygons, then quarterly and network-type summaries were rebuilt from the records. The existing NDT7 exports were compared with the rebuilt outputs.",
        "",
        "## Geographic reassignment",
        "",
        "| Country | GeoBoundary ADM1 features | Unique coordinates | Nearest fallback | Crosswalk outliers (mapped downloads) | Unmapped downloads | Outlier percent of mapped downloads |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in diagnostics:
        lines.append(
            f"| {item['country']} | {item['boundary_features']} | {item['unique_coordinates']:,} | {item['nearest_fallback_coordinates']:,} | {item['changed_assignment_download_tests']:,} | {item['unmapped_download_tests']:,} | {item['changed_assignment_percent']:.4f}% |"
        )
    lines.extend(
        [
            "",
            "## Existing export comparison",
            "",
            "| Country | Network | Existing rows | Duplicate area-quarter keys | Existing test sum | Rebuilt test sum | Area-quarter keys with a count or download-speed change | Largest download-speed difference (Mbps) |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for item in comparisons:
        lines.append(
            f"| {item['country']} | {item['network_type']} | {item['old_export_rows']:,} | {item['old_duplicate_area_quarter_keys']} | {item['old_tests_sum']:,} | {item['new_tests_sum']:,} | {item['different_area_quarter_keys']:,} | {item['max_abs_download_mean_difference_mbps']:.6f} |"
        )
    total_changed = sum(int(item["changed_assignment_download_tests"]) for item in diagnostics)
    total_download = sum(int(item["total_download_tests"]) for item in diagnostics)
    total_unmapped_download = sum(int(item["unmapped_download_tests"]) for item in diagnostics)
    any_old_diff = any(item["different_area_quarter_keys"] or item["old_tests_sum"] != item["new_tests_sum"] for item in comparisons)
    lines.extend(
        [
            "",
            "## RQ rerun decision",
            "",
            f"- Download observations whose coordinate result disagrees with the old-area-to-GeoBoundary crosswalk: **{total_changed:,} / {total_download:,}** mapped observations across the nine countries.",
            f"- Download observations without enough coordinate or area information for any ADM1 assignment: **{total_unmapped_download:,}**.",
            f"- Existing broadband/cellular area-quarter outputs differ from the rebuilt GeoBoundary outputs: **{any_old_diff}**.",
            "- A country-level total or country-wide mean is invariant to reassignment when the same records and filters are used. Any RQ based on province/region results should be refreshed if the comparison reports different area-quarter keys or metrics.",
            "- Myanmar’s existing broadband export contains duplicate Mandalay-quarter rows, caused by folding Naypyitaw into Mandalay before joining download and upload aggregates. The remap rebuilds those summaries from the clean parquet records, preventing the existing export’s duplicate rows from being counted twice.",
            "",
            "## Mapping choices and limits",
            "",
            "- The Philippines is spatially assigned directly to the 17 GeoBoundary ADM1 regions.",
            "- Myanmar has no separate Naypyidaw ADM1 feature in the supplied layer; the existing workflow’s documented convention folds Naypyitaw into Mandalay.",
            "- Coordinate groups outside all polygons are assigned to the nearest ADM1 polygon in an equal-area projection and are counted in the nearest-fallback column.",
            "- GeoBoundary features with no data are retained in the GeoJSON with zero observation counts and null performance metrics.",
            "",
            "## Files",
            "",
            f"- `{quarterly_path.as_posix()}` — all available area × quarter × network-type metrics after GeoBoundary spatial reassignment.",
            f"- `{geojson_path.as_posix()}` — one feature per ADM1 with pooled network-type metrics.",
            f"- `{crosswalk_path.as_posix()}` — old area label to new boundary assignments.",
            f"- `{changes_path.as_posix()}` — reassignment test counts by old and new area.",
            f"- `{compare_path.as_posix()}` — current export versus rebuilt summary comparison.",
            f"- `{unmapped_path.as_posix()}` — coordinate groups that could not be mapped without inventing a location.",
        ]
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    con.close()
    print(f"Wrote {quarterly_path}")
    print(f"Wrote {geojson_path}")
    print(f"Wrote {crosswalk_path}")
    print(f"Wrote {changes_path}")
    print(f"Wrote {compare_path}")
    print(f"Wrote {unmapped_path}")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
