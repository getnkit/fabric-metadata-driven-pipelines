"""Build C12 and O02 from genuine screenshot pixels without resizing.

Reproduce from the repository root:
    python -m pip install Pillow==11.3.0
    python scripts/evidence/build_sftp_composites.py

Rebuild only O02:
    python -c "from scripts.evidence.build_sftp_composites import build_o02; build_o02()"

O02 uses separated UI crops to omit operational/environment identifiers.
Crop boxes are (left, top, right, bottom); destination rectangles are (x, y, w, h).
"""

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version


ROOT = Path(__file__).resolve().parents[2]
BASE = Path("docs/assets/screenshots")
BACKGROUND = "#F4F5F6"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def label(canvas, xy, value, size=19):
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=size)
    if draw.textbbox(xy, value, font=font)[2] > canvas.width - 20:
        raise ValueError("Label exceeds canvas width")
    draw.text(xy, value, font=font, fill="#263238")


def paste_source(canvas, path, crops):
    with Image.open(ROOT / path) as source:
        source.load()
        if "A" in source.getbands() and source.getchannel("A").getextrema() != (255, 255):
            raise ValueError(f"Unexpected transparency in {path}")
        source = source.convert("RGB")
        placements = []
        for box, destination in crops:
            box = box or (0, 0, source.width, source.height)
            if not (0 <= box[0] < box[2] <= source.width
                    and 0 <= box[1] < box[3] <= source.height):
                raise ValueError(f"Invalid crop for {path}")
            pixels = source.crop(box)
            canvas.paste(pixels, destination)
            placements.append({"crop_box": list(box),
                               "rectangle": [*destination, *pixels.size]})
        return {"path": path.as_posix(), "sha256": digest(ROOT / path),
                "dimensions": list(source.size), "placements": placements}


def save(canvas, candidate, filename, sources, claim, limitations):
    output = BASE / "composites" / filename
    (ROOT / output).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(ROOT / output, format="PNG", compress_level=9)
    manifest = {
        "candidate": candidate,
        "asset_role": "derived_composite",
        "publication_decision": "owner_approved_with_evidence_limitations",
        "output": output.as_posix(),
        "output_dimensions": list(canvas.size),
        "output_sha256": digest(ROOT / output),
        "generator": Path(__file__).relative_to(ROOT).as_posix(),
        "pillow_version": pillow_version,
        "presentation": "Composite of DEV evidence; native pixels; no resizing or retouching.",
        "supported_claim": claim,
        "limitations": limitations,
        "sources": sources,
    }
    (ROOT / output).with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Created {output} ({canvas.width}x{canvas.height}) and manifest")


def build_c12():
    source_dir = BASE / "supporting/s4-sftp-incremental"
    panels = [
        ("1. Watermark Before", "cx-s4-watermark-before.png"),
        ("2. SUCCESS Audit Record", "cx-s4-audit-success.png"),
        ("3. Bronze Source-File Lineage", "cx-s4-bronze-new-file-lineage.png"),
        ("4. Watermark After", "cx-s4-watermark-after.png"),
    ]
    sizes = []
    for _, filename in panels:
        with Image.open(ROOT / source_dir / filename) as source:
            sizes.append(source.size)
    width = max(size[0] for size in sizes) + 40
    footer_y = 124 + sum(34 + height + 28 for _, height in sizes)
    canvas = Image.new("RGB", (width, footer_y + 104), BACKGROUND)
    label(canvas, (20, 22), "C12 | Composite of DEV evidence", 30)
    label(canvas, (20, 70), "Audit, Bronze lineage and checkpoint comparison - not a single-run trace.")
    sources, cursor = [], 124
    for (heading, filename), (_, height) in zip(panels, sizes):
        label(canvas, (20, cursor), heading, 23)
        sources.append(paste_source(canvas, source_dir / filename,
                                    [(None, (20, cursor + 34))]))
        cursor += 34 + height + 28
    limitation = ("Run type is not visible; some run identifiers are truncated. "
                  "Exact execution correlation is not independently verified.")
    ImageDraw.Draw(canvas).rectangle((20, footer_y, width - 20, footer_y + 82), fill="#E6E9EC")
    label(canvas, (32, footer_y + 14), "Run type is not visible; some run identifiers are truncated.", 18)
    label(canvas, (32, footer_y + 45), "Exact execution correlation is not independently verified.", 18)
    save(canvas, "C12", "c12-sftp-new-file-incremental.png", sources,
         "The DEV movement audit reports SUCCESS and six processed rows. Six visible Bronze "
         "rows share the after-state Batch ID. The checkpoint advances from "
         "2026-10-23T12:31:47.787Z to 2026-10-24T02:04:02.238Z.",
         [limitation, "Remote file Last Modified values are not visible.",
          "C08/C09 depict a different DEV execution example."])


def build_o02():
    source_dir = BASE / "supporting/optional/o02-file-row-count"
    canvas = Image.new("RGB", (1362, 726), BACKGROUND)
    label(canvas, (20, 22), "O02 | Composite of DEV evidence", 30)
    label(canvas, (20, 70), "File-transfer metrics and parsed-row metrics from selected source UI crops.")
    label(canvas, (20, 124), "Binary Copy | files", 23)
    label(canvas, (695, 124), "Notebook | parsed rows", 23)
    sources = [paste_source(canvas, source_dir / "cx-o02-binary-copy.png",
                            [((1073, 18, 1720, 422), (20, 164))])]
    label(canvas, (695, 164), "Selected activity", 18)
    label(canvas, (695, 302), "Parsed row metrics (original line wrap)", 18)
    ImageDraw.Draw(canvas).rectangle((695, 334, 1015, 392), fill="white")
    # Clip surrounding metadata from each line of the serialized metrics object.
    # Both strips use the SAME source-to-canvas translation: no token reflow,
    # joining of labels/values, or reconstruction of source UI text.
    metric_boxes = [(1288, 725, 1564, 741), (1262, 744, 1278, 758)]
    metric_crops = [(box, (box[0] - 553, box[1] - 381)) for box in metric_boxes]
    sources.append(paste_source(canvas, source_dir / "cx-o02-notebook-parse.png", [
        ((90, 835, 545, 867), (695, 196)),
        ((1255, 562, 1340, 588), (695, 252)),
        *metric_crops,
    ]))
    sources[-1]["crop_method"] = (
        "Serialized metrics object clipped line by line, retaining original relative "
        "positions and wrapping. Surrounding output metadata omitted; no token reflow "
        "or text reconstruction. Activity and Output heading are separate context crops."
    )
    label(canvas, (695, 420), "Native pixel excerpt; original line positions.", 18)
    label(canvas, (695, 448), "Surrounding output metadata omitted.", 18)
    ImageDraw.Draw(canvas).rectangle((20, 594, 1342, 704), fill="#E6E9EC")
    label(canvas, (32, 608), "Both Notebook row metrics reuse the same parsed DataFrame count.", 18)
    label(canvas, (32, 638), "They are not an independent Bronze recount.", 18)
    label(canvas, (32, 668), "End-to-end execution correlation is not independently verified.", 18)
    save(canvas, "O02", "o02-file-vs-row-count.png", sources,
         "Binary Copy reports one file read and one written; the Notebook reports six "
         "source rows and six target rows. These are different measurement units.",
         ["Both Notebook row metrics reuse one parsed DataFrame count; no independent Bronze recount.",
          "End-to-end execution correlation is not independently verified.",
          "Separated native UI crops omit operational/environment identifiers and intervening metadata."])


if __name__ == "__main__":
    build_c12()
    build_o02()
