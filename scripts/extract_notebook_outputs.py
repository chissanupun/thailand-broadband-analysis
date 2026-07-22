#!/usr/bin/env python3
"""Dump every code-cell output (image/png, text/html, text/plain, stderr) from
.ipynb files into notebook_outputs/<notebook path>/, one file per output.

Reads raw notebook JSON only (no nbformat dependency, no re-execution) so it's
safe to run against large already-executed notebooks.

Usage:
    python3 scripts/extract_notebook_outputs.py                # all notebooks/
    python3 scripts/extract_notebook_outputs.py path/to/nb.ipynb [more.ipynb ...]
"""
import base64
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
OUT_ROOT = REPO_ROOT / "notebook_outputs"

MIME_EXT = {
    "image/png": ("png", True),
    "image/jpeg": ("jpg", True),
    "image/svg+xml": ("svg", False),
    "text/html": ("html", False),
    "text/plain": ("txt", False),
    "application/vnd.plotly.v1+json": ("plotly.json", False),
}


def _as_text(value):
    return "".join(value) if isinstance(value, list) else str(value)


def extract_notebook(nb_path: Path):
    with nb_path.open(encoding="utf-8") as f:
        nb = json.load(f)

    rel = nb_path.relative_to(NOTEBOOKS_DIR).with_suffix("")
    dest_dir = OUT_ROOT / rel
    written = 0

    for cell_idx, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        outputs = cell.get("outputs") or []
        if not outputs:
            continue

        for out_idx, out in enumerate(outputs):
            otype = out.get("output_type")
            data = out.get("data")

            if otype == "stream":
                text = _as_text(out.get("text", ""))
                if not text.strip():
                    continue
                stream = out.get("name", "stdout")
                dest_dir.mkdir(parents=True, exist_ok=True)
                fname = f"cell{cell_idx:04d}_out{out_idx}_{stream}.txt"
                (dest_dir / fname).write_text(text, encoding="utf-8")
                written += 1
                continue

            if otype == "error":
                text = "\n".join(out.get("traceback") or [])
                if not text.strip():
                    continue
                dest_dir.mkdir(parents=True, exist_ok=True)
                fname = f"cell{cell_idx:04d}_out{out_idx}_error.txt"
                (dest_dir / fname).write_text(text, encoding="utf-8")
                written += 1
                continue

            if otype not in ("execute_result", "display_data") or not data:
                continue

            # prefer richest mime type available per output
            for mime, (ext, is_b64) in MIME_EXT.items():
                if mime not in data:
                    continue
                dest_dir.mkdir(parents=True, exist_ok=True)
                fname = f"cell{cell_idx:04d}_out{out_idx}.{ext}"
                dest_path = dest_dir / fname
                if is_b64:
                    raw = base64.b64decode(_as_text(data[mime]))
                    dest_path.write_bytes(raw)
                else:
                    dest_path.write_text(_as_text(data[mime]), encoding="utf-8")
                written += 1
                break  # one file per output, richest mime wins

    return written


def main(argv):
    if argv:
        targets = [Path(a).resolve() for a in argv]
    else:
        targets = sorted(
            p for p in NOTEBOOKS_DIR.rglob("*.ipynb")
            if ".ipynb_checkpoints" not in p.parts
        )

    total = 0
    for nb_path in targets:
        n = extract_notebook(nb_path)
        total += n
        print(f"{nb_path.relative_to(REPO_ROOT)}: {n} outputs")

    print(f"\nTotal: {total} outputs written under {OUT_ROOT.relative_to(REPO_ROOT)}/")


if __name__ == "__main__":
    main(sys.argv[1:])
