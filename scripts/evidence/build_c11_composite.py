"""Build C11 without cropping, resizing, or rewriting screenshot pixels.

Reproduce from the repository root:
    python -m pip install Pillow==11.3.0
    python scripts/evidence/build_c11_composite.py

Pillow's bundled font avoids dependencies on workstation fonts.
"""

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path("docs/assets/screenshots/supporting/s3-sql-incremental")
OUTPUT = Path("docs/assets/screenshots/composites/c11-sql-server-incremental.png")
PANELS = [
    ("1. Watermark Before", SOURCE / "cx-s3-watermark-before.png"),
    ("2. SUCCESS Audit Records", SOURCE / "cx-s3-audit-success.png"),
    ("3. Watermark After", SOURCE / "cx-s3-watermark-after.png"),
]
TITLE = "C11 | Composite of DEV evidence"
SUBTITLE = "Audit and checkpoint comparison - not a single-run execution trace."
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

    margin, heading_height, gap = 20, 34, 28
    width = max(image.width for image in images) + 2 * margin
    cursor = 124
    sources = []
    for (label, path), image in zip(PANELS, images):
        sources.append({
            "path": path.as_posix(),
            "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest(),
            "label": label,
            "heading_y": cursor,
            "rectangle": [margin, cursor + heading_height, image.width, image.height],
        })
        cursor += heading_height + image.height + gap

    canvas = Image.new("RGB", (width, cursor + 76), "#F4F5F6")
    draw = ImageDraw.Draw(canvas)

    def text(position, value, size, color="#263238"):
        font = ImageFont.load_default(size=size)
        if draw.textbbox(position, value, font=font)[2] > width - margin:
            raise ValueError("Label exceeds canvas width")
        draw.text(position, value, font=font, fill=color)

    text((margin, 22), TITLE, 30)
    text((margin, 70), SUBTITLE, 19, "#53616B")
    for source, image in zip(sources, images):
        text((margin, source["heading_y"]), source["label"], 23)
        canvas.paste(image, tuple(source["rectangle"][:2]))
    draw.rectangle((margin, cursor, width - margin, cursor + 54), fill="#E6E9EC")
    text((margin + 12, cursor + 16), LIMITATION, 18)

    output = ROOT / OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, format="PNG", compress_level=9)
    manifest = {
        "candidate": "C11",
        "asset_role": "derived_composite",
        "publication_decision": "owner_approved_with_evidence_limitations",
        "output": OUTPUT.as_posix(),
        "output_dimensions": list(canvas.size),
        "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "generator": Path(__file__).relative_to(ROOT).as_posix(),
        "pillow_version": pillow_version,
        "title": TITLE,
        "subtitle": SUBTITLE,
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
