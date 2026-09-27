# NDT7 GeoBoundaries ADM1 remapping check

The nine cleaned NDT7 parquet datasets were read without modification. Distinct coordinates were assigned to the supplied country ADM1 polygons, then quarterly and network-type summaries were rebuilt from the records. The existing NDT7 exports were compared with the rebuilt outputs.

## Geographic reassignment

| Country | GeoBoundary ADM1 features | Unique coordinates | Nearest fallback | Crosswalk outliers (mapped downloads) | Unmapped downloads | Outlier percent of mapped downloads |
|---|---:|---:|---:|---:|---:|---:|
| Cambodia | 25 | 48 | 3 | 0 | 0 | 0.0000% |
| Indonesia | 34 | 2,760 | 128 | 10,300 | 3,874 | 0.0049% |
| Laos | 18 | 33 | 1 | 0 | 0 | 0.0000% |
| Malaysia | 16 | 1,072 | 44 | 182,115 | 0 | 5.1279% |
| Myanmar | 14 | 62 | 2 | 0 | 0 | 0.0000% |
| Philippines | 17 | 2,196 | 371 | 598,916 | 15 | 0.4007% |
| Singapore | 5 | 139 | 5 | 0 | 0 | 0.0000% |
| Thailand | 77 | 1,298 | 18 | 0 | 4 | 0.0000% |
| Vietnam | 64 | 900 | 17 | 153,761 | 0 | 1.2088% |

## Existing export comparison

| Country | Network | Existing rows | Duplicate area-quarter keys | Existing test sum | Rebuilt test sum | Area-quarter keys with a count or download-speed change | Largest download-speed difference (Mbps) |
|---|---|---:|---:|---:|---:|---:|---:|
| Cambodia | broadband | 188 | 0 | 263,722 | 263,722 | 0 | 0.000000 |
| Cambodia | cellular | 37 | 0 | 157,176 | 157,176 | 0 | 0.000000 |
| Indonesia | broadband | 404 | 0 | 135,260,905 | 135,260,905 | 18 | 0.008424 |
| Indonesia | cellular | 368 | 0 | 53,843,486 | 53,843,486 | 2 | 0.000006 |
| Laos | broadband | 149 | 0 | 38,757 | 38,757 | 0 | 0.000000 |
| Laos | cellular | 41 | 0 | 27,582 | 27,582 | 0 | 0.000000 |
| Malaysia | broadband | 190 | 0 | 2,215,382 | 2,215,382 | 42 | 111.588248 |
| Malaysia | cellular | 116 | 0 | 1,148,539 | 1,148,539 | 26 | 12.381319 |
| Myanmar | broadband | 114 | 6 | 1,018,167 | 946,013 | 6 | 0.000000 |
| Myanmar | cellular | 53 | 0 | 190,051 | 190,051 | 0 | 0.000000 |
| Philippines | broadband | 204 | 0 | 104,607,087 | 105,039,509 | 93 | 67.517297 |
| Philippines | cellular | 159 | 0 | 40,725,976 | 40,725,976 | 16 | 0.138018 |
| Singapore | broadband | 55 | 0 | 10,097,944 | 10,097,944 | 0 | 0.000000 |
| Singapore | cellular | 47 | 0 | 2,256,346 | 2,256,346 | 0 | 0.000000 |
| Thailand | broadband | 902 | 0 | 19,991,483 | 19,991,483 | 0 | 0.000000 |
| Thailand | cellular | 494 | 0 | 14,814,447 | 14,814,447 | 0 | 0.000000 |
| Vietnam | broadband | 746 | 0 | 11,219,173 | 11,219,173 | 219 | 60.428941 |
| Vietnam | cellular | 308 | 0 | 585,730 | 585,730 | 30 | 6.904578 |

## RQ rerun decision

- Download observations whose coordinate result disagrees with the old-area-to-GeoBoundary crosswalk: **945,092 / 434,137,087** mapped observations across the nine countries.
- Download observations without enough coordinate or area information for any ADM1 assignment: **3,893**.
- Existing broadband/cellular area-quarter outputs differ from the rebuilt GeoBoundary outputs: **True**.
- A country-level total or country-wide mean is invariant to reassignment when the same records and filters are used. Any RQ based on province/region results should be refreshed if the comparison reports different area-quarter keys or metrics.
- Myanmar’s existing broadband export contains duplicate Mandalay-quarter rows, caused by folding Naypyitaw into Mandalay before joining download and upload aggregates. The remap rebuilds those summaries from the clean parquet records, preventing the existing export’s duplicate rows from being counted twice.

## Mapping choices and limits

- The Philippines is spatially assigned directly to the 17 GeoBoundary ADM1 regions.
- Myanmar has no separate Naypyidaw ADM1 feature in the supplied layer; the existing workflow’s documented convention folds Naypyitaw into Mandalay.
- Coordinate groups outside all polygons are assigned to the nearest ADM1 polygon in an equal-area projection and are counted in the nearest-fallback column.
- GeoBoundary features with no data are retained in the GeoJSON with zero observation counts and null performance metrics.

## Files

- `data/exports/ndt7_geoboundaries_adm1_quarterly.csv` — all available area × quarter × network-type metrics after GeoBoundary spatial reassignment.
- `data/geo/ndt7_geoboundaries_adm1_summary.geojson` — one feature per ADM1 with pooled network-type metrics.
- `data/exports/ndt7_geoboundaries_adm1_crosswalk.csv` — old area label to new boundary assignments.
- `data/exports/ndt7_geoboundaries_adm1_assignment_changes.csv` — reassignment test counts by old and new area.
- `data/exports/ndt7_geoboundaries_adm1_existing_export_comparison.csv` — current export versus rebuilt summary comparison.
- `data/exports/ndt7_geoboundaries_unmapped_coordinate_groups.csv` — coordinate groups that could not be mapped without inventing a location.
