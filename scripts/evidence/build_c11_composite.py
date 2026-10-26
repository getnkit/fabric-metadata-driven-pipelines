"""Build C11 without cropping, resizing, or rewriting screenshot pixels.

Reproduce from the repository root:
    python -m pip install Pillow==11.3.0
    python scripts/evidence/build_c11_composite.py

The shared style records the local font hash; set EVIDENCE_FONT_PATH to reproduce it.
"""

import hashlib
import json
from pathlib import Path

from PIL import Image, __version__ as pillow_version

if __package__:
    from . import composite_style as style
else:
    import composite_style as style


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path("docs/assets/screenshots/supporting/s3-sql-incremental")
OUTPUT = Path("docs/assets/screenshots/composites/c11-sql-server-incremental.png")
PANELS = [
    ("Earlier checkpoint values", SOURCE / "cx-s3-watermark-before.png"),
    ("SUCCESS audit records", SOURCE / "cx-s3-audit-success.png"),
    ("Later checkpoint values", SOURCE / "cx-s3-watermark-after.png"),
]
TITLE = "SQL Server Incremental - Audit and Watermark Evidence"
LIMITATION = (
    "Run type is not visible; exact execution correlation is not independently verified."
)
CLAIM = (
    "Four DEV SUCCESS audit rows contain processing bounds consistent with the "
    "displayed before/after checkpoint values, and those checkpoint values advanced."
)


def main():
    images = []
    for _, path in PANELS:
        with Image.open(ROOT / path) as image:
            image.load()
            if "A" in image.getbands() and image.getchannel("A").getextrema() != (255, 255):
                raise ValueError(f"Unexpected transparency in {path}")
            images.append(image.convert("RGB"))

    width, height, panels = style.vertical_layout([image.size for image in images])
    sources = []
    for (label, path), image, panel in zip(PANELS, images, panels):
        sources.append({
            "path": path.as_posix(),
            "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest(),
            "dimensions": list(image.size),
            "label": label,
            **panel,
        })

    canvas = Image.new("RGB", (width, height), style.BACKGROUND)
    style.label(canvas, (style.MARGIN, 20), TITLE, style.TITLE_SIZE, style.TEXT)
    for source, image in zip(sources, images):
        style.card(canvas, source["card_rectangle"], source["label"])
        canvas.paste(image, tuple(source["rectangle"][:2]))

    output = ROOT / OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, format="PNG", compress_level=9)
    manifest = {
        "candidate": "C11",
        "asset_role": "derived_composite",
        "publication_decision": "owner_approved_with_evidence_limitations",
        "presentation_review": "pending_owner_review",
        "output": OUTPUT.as_posix(),
        "output_dimensions": list(canvas.size),
        "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "generator": Path(__file__).relative_to(ROOT).as_posix(),
        "pillow_version": pillow_version,
        "visual_style": style.metadata(),
        "title": TITLE,
        "subtitle": None,
        "on_image_notes": [],
        "limitation": LIMITATION,
        "supported_claim": CLAIM,
        "sources": sources,
    }
    output.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Created {OUTPUT} ({canvas.width}x{canvas.height}) and manifest")


if __name__ == "__main__":
    main()
