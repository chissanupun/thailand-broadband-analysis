"""Build demo/geo.json: simplified province shapes + dissolved country outlines for the demo map.

Province names already match demo/data.json exactly (checked: 0 unmatched in all 9 countries).
Run: uv run --with shapely python scripts/build_demo_geo.py
"""
import json
from pathlib import Path

from shapely.geometry import mapping, shape
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parent.parent
GEO = ROOT / 'data' / 'geo'
OUT = ROOT / 'demo' / 'geo.json'
FILES = {'Thailand': 'thailand', 'Vietnam': 'vietnam', 'Philippines': 'philippines', 'Cambodia': 'cambodia',
         'Laos': 'laos', 'Malaysia': 'malaysia', 'Myanmar': 'myanmar', 'Indonesia': 'indonesia', 'Singapore': 'singapore'}
PROV_TOL, COUNTRY_TOL, MIN_AREA = 0.01, 0.03, 0.002  # degrees; drops tiny islets


def rings(geom, digits=3):
    polys = [geom] if geom.geom_type == 'Polygon' else list(geom.geoms)
    out = []
    for p in polys:
        if p.area < MIN_AREA:
            continue
        out.append([[round(x, digits), round(y, digits)] for x, y in p.exterior.coords])
    return out


def main():
    out = {}
    for country, f in FILES.items():
        feats = json.loads((GEO / f'{f}_provinces.geojson').read_text(encoding='utf-8'))['features']
        shapes = {ft['properties']['name']: shape(ft['geometry']).buffer(0) for ft in feats}
        # Singapore is tiny; keep more detail there
        tol = PROV_TOL / 10 if country == 'Singapore' else PROV_TOL
        provinces = {n: rings(g.simplify(tol, preserve_topology=True), 4 if country == 'Singapore' else 3) for n, g in shapes.items()}
        outline = unary_union(list(shapes.values())).simplify(COUNTRY_TOL / (10 if country == 'Singapore' else 1))
        out[country] = {'outline': rings(outline), 'provinces': {n: r for n, r in provinces.items() if r}}
        print(country, len(out[country]['provinces']), 'provinces')
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f'wrote {OUT} ({OUT.stat().st_size // 1024} KB)')


if __name__ == '__main__':
    main()
