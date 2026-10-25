"""Build C10/C13 from native screenshot pixels, displaying duplicate state once.

Reproduce from the repository root:
    python -m pip install Pillow==11.3.0
    python scripts/evidence/build_incremental_composites.py

Both watermark source files are preserved and recorded. Composition stops if
their bytes differ; identical files are not independent before/after evidence.
Pillow's bundled font avoids dependencies on workstation fonts.
"""

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version


ROOT = Path(__file__).resolve().parents[2]
BASE = Path("docs/assets/screenshots")
SPECS = [
    {
        "candidate": "C10",
        "directory": "s2-no-new-data",
        "output": "c10-no-new-data-skipped.png",
        "title": "No New Data - SKIPPED Audit and Checkpoint Context",
        "subtitle": "C10 · DEV evidence composite",
        "panels": [
            ("SKIPPED audit records", "cx-s2-skipped-audit.png"),
            ("Bronze count result - query scope not shown", "cx-s2-no-bronze-append.png"),
            ("Watermark state - duplicate source files shown once", "cx-s2-watermark-before.png"),
        ],
        "duplicate": "cx-s2-watermark-after.png",
        "supported_claim": (
            "DEV customers and inventory_movement audits report SKIPPED with zero "
            "source/target rows. A separate Bronze result lists bronze_rows = 0 with "
            "no visible query scope. The watermark source files are byte-identical."
        ),
        "limitations": [
            "Byte-identical watermark source files do not establish independent before/after observations.",
            "Bronze query/filter is not visible; the zero count does not independently prove no append.",
            "Run type is not shown; some Run IDs are truncated. Exact execution correlation is unverified.",
        ],
    },
    {
        "candidate": "C13",
        "directory": "s5-backfill",
        "output": "c13-incremental-backfill.png",
        "title": "BACKFILL - Audit and Checkpoint Evidence",
        "subtitle": "C13 · DEV evidence composite",
        "panels": [
            ("BACKFILL / INCREMENTAL - SUCCESS audit", "cx-s5-audit-backfill.png"),
            ("Watermark state - duplicate source files shown once", "cx-s5-watermark-before.png"),
        ],
        "duplicate": "cx-s5-watermark-after.png",
        "supported_claim": (
            "The DEV customers audit records run_type BACKFILL, load_strategy INCREMENTAL, "
            "SUCCESS, and source/target counts of 2/2. Both watermark source files display "
            "2026-10-24T01:08:00.941Z and are byte-identical."
        ),
        "limitations": [
            "Byte-identical watermark source files do not establish independent before/after observations.",
            "Audit LOW/HIGH and Batch ID are truncated; the complete processing window is unavailable.",
            "Checkpoint non-advancement, Bronze append and exact execution correlation are unverified.",
            "Exactly-once business semantics are not established.",
        ],
    },
]


def build(spec):
    directory = BASE / "supporting" / spec["directory"]
    sources, images = [], {}
    for filename in [name for _, name in spec["panels"]] + [spec["duplicate"]]:
        path = directory / filename
        data = (ROOT / path).read_bytes()
        with Image.open(ROOT / path) as source:
            source.load()
            if "A" in source.getbands() and source.getchannel("A").getextrema() != (255, 255):
                raise ValueError(f"Unexpected transparency in {path}")
            images[filename] = source.convert("RGB")
        sources.append({
            "path": path.as_posix(),
            "sha256": hashlib.sha256(data).hexdigest(),
            "dimensions": list(images[filename].size),
            "displayed": filename != spec["duplicate"],
            "placements": [],
        })

    original = directory / spec["panels"][-1][1]
    duplicate = directory / spec["duplicate"]
    if (ROOT / original).read_bytes() != (ROOT / duplicate).read_bytes():
        raise ValueError("Watermark sources differ; review required before displaying state once")
    sources[-1]["duplicate_of"] = original.as_posix()
    sources[-1]["omission_reason"] = "Byte-identical watermark displayed once; not a separate observation."

    width, cursor = max(image.width for image in images.values()) + 40, 124
    for (heading, filename), source in zip(spec["panels"], sources):
        image = images[filename]
        source["heading"] = heading
        source["heading_y"] = cursor
        source["placements"] = [{"rectangle": [20, cursor + 34, image.width, image.height]}]
        cursor += 34 + image.height + 28

    canvas = Image.new("RGB", (width, cursor + 36 + 30 * len(spec["limitations"])), "#F4F5F6")
    draw = ImageDraw.Draw(canvas)

    def text(xy, value, size, color="#263238"):
        font = ImageFont.load_default(size=size)
        box = draw.textbbox(xy, value, font=font)
        if box[2] > width - 20 or box[3] > canvas.height - 20:
            raise ValueError("Label exceeds canvas bounds")
        draw.text(xy, value, font=font, fill=color)

    title = spec["title"]
    text((20, 22), title, 30)
    text((20, 70), spec["subtitle"], 19, "#53616B")
    for (_, filename), source in zip(spec["panels"], sources):
        text((20, source["heading_y"]), source["heading"], 23)
        canvas.paste(images[filename], tuple(source["placements"][0]["rectangle"][:2]))
    draw.line((20, cursor, width - 20, cursor), fill="#CDD5DD")
    for index, limitation in enumerate(spec["limitations"]):
        text((20, cursor + 14 + index * 30), limitation, 18, "#53616B")

    output = BASE / "composites" / spec["output"]
    (ROOT / output).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(ROOT / output, format="PNG", compress_level=9)
    manifest = {
        "candidate": spec["candidate"],
        "asset_role": "derived_composite",
        "publication_decision": "owner_approved_with_evidence_limitations",
        "presentation_review": "pending_owner_review",
        "output": output.as_posix(),
        "output_dimensions": list(canvas.size),
        "output_sha256": hashlib.sha256((ROOT / output).read_bytes()).hexdigest(),
        "generator": Path(__file__).relative_to(ROOT).as_posix(),
        "pillow_version": pillow_version,
        "title": title,
        "subtitle": spec["subtitle"],
        "presentation": "Complete native screenshot panels; no cropping, resizing, retouching, or timeline arrows.",
        "supported_claim": spec["supported_claim"],
        "limitations": spec["limitations"],
        "watermark_duplicate_handling": {
            "source_paths": [original.as_posix(), duplicate.as_posix()],
            "byte_identical": True,
            "display_count": 1,
            "independent_before_after_observations_verified": False,
        },
        "sources": sources,
    }
    (ROOT / output).with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Created {output} ({canvas.width}x{canvas.height}) and manifest")


if __name__ == "__main__":
    for spec in SPECS:
        build(spec)
