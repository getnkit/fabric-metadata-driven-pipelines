"""Build C12/O02 from genuine screenshots; O02 metrics use integer enlargement.

Reproduce from the repository root:
    python -m pip install Pillow==11.3.0
    python scripts/evidence/build_sftp_composites.py

Rebuild only O02:
    python -c "from scripts.evidence.build_sftp_composites import build_o02; build_o02()"

O02 uses separated UI crops to omit operational/environment identifiers.
Only its metrics strips are enlarged 2x with NEAREST (exact pixel replication).
Crop boxes are (left, top, right, bottom); destination rectangles are (x, y, w, h).
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
BASE = Path("docs/assets/screenshots")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def paste_source(canvas, path, crops):
    with Image.open(ROOT / path) as source:
        source.load()
        if "A" in source.getbands() and source.getchannel("A").getextrema() != (255, 255):
            raise ValueError(f"Unexpected transparency in {path}")
        source = source.convert("RGB")
        placements = []
        for crop in crops:
            box, destination = crop[:2]
            scale = crop[2] if len(crop) == 3 else 1
            if not isinstance(scale, int) or scale < 1:
                raise ValueError("Only integer pixel replication is supported")
            box = box or (0, 0, source.width, source.height)
            if not (0 <= box[0] < box[2] <= source.width
                    and 0 <= box[1] < box[3] <= source.height):
                raise ValueError(f"Invalid crop for {path}")
            pixels = source.crop(box)
            if scale != 1:
                pixels = pixels.resize((pixels.width * scale, pixels.height * scale),
                                       Image.Resampling.NEAREST)
            canvas.paste(pixels, destination)
            placements.append({"crop_box": list(box),
                               "scale": scale, "resampling": "NEAREST" if scale != 1 else "none",
                               "rectangle": [*destination, *pixels.size]})
        return {"path": path.as_posix(), "sha256": digest(ROOT / path),
                "dimensions": list(source.size), "placements": placements}


def save(canvas, candidate, filename, sources, claim, limitations, title, notes=()):
    output = BASE / "composites" / filename
    (ROOT / output).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(ROOT / output, format="PNG", compress_level=9)
    manifest = {
        "candidate": candidate,
        "asset_role": "derived_composite",
        "publication_decision": "owner_approved_with_evidence_limitations",
        "presentation_review": "pending_owner_review",
        "output": output.as_posix(),
        "output_dimensions": list(canvas.size),
        "output_sha256": digest(ROOT / output),
        "generator": Path(__file__).relative_to(ROOT).as_posix(),
        "pillow_version": pillow_version,
        "visual_style": style.metadata(),
        "title": title,
        "subtitle": None,
        "on_image_notes": list(notes),
        "presentation": (
            "DEV evidence composite; complete native panels; no cropping, resizing or retouching."
            if candidate == "C12" else
            "DEV evidence composite; genuine UI crops; metrics enlarged 2x with NEAREST; no retouching or token reflow."
        ),
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
        ("Earlier checkpoint values", "cx-s4-watermark-before.png"),
        ("SUCCESS audit record", "cx-s4-audit-success.png"),
        ("Bronze source-file lineage", "cx-s4-bronze-new-file-lineage.png"),
        ("Later checkpoint values", "cx-s4-watermark-after.png"),
    ]
    sizes = []
    for _, filename in panels:
        with Image.open(ROOT / source_dir / filename) as source:
            sizes.append(source.size)
    width, height, layout = style.vertical_layout(sizes)
    canvas = Image.new("RGB", (width, height), style.BACKGROUND)
    title = "SFTP Incremental - Bronze Lineage and Checkpoint Context"
    style.label(canvas, (style.MARGIN, 20), title, style.TITLE_SIZE, style.TEXT)
    sources = []
    for (heading, filename), panel in zip(panels, layout):
        style.card(canvas, panel["card_rectangle"], heading)
        source = paste_source(canvas, source_dir / filename,
                              [(None, tuple(panel["rectangle"][:2]))])
        source["heading"] = heading
        source["heading_y"] = panel["heading_y"]
        source["card_rectangle"] = panel["card_rectangle"]
        sources.append(source)
    limitation = ("Run type is not visible; some run identifiers are truncated. "
                  "Exact execution correlation is not independently verified.")
    save(canvas, "C12", "c12-sftp-new-file-incremental.png", sources,
         "The DEV movement audit reports SUCCESS and six processed rows. Six visible Bronze "
         "rows share the after-state Batch ID. The checkpoint advances from "
         "2026-10-23T12:31:47.787Z to 2026-10-24T02:04:02.238Z.",
         [limitation, "Remote file Last Modified values are not visible.",
          "C08/C09 depict a different DEV execution example."], title)


def build_o02():
    source_dir = BASE / "supporting/optional/o02-file-row-count"
    canvas = Image.new("RGB", (1386, 530), style.BACKGROUND)
    title = "SFTP Ingestion - Files Transferred vs Rows Parsed"
    style.label(canvas, (style.MARGIN, 20), title, style.TITLE_SIZE, style.TEXT)
    cards = [[20, 64, 667, 446], [699, 64, 667, 224]]
    style.card(canvas, cards[0], "Binary Copy file counts")
    style.card(canvas, cards[1], "Notebook row counts")
    sources = [paste_source(canvas, source_dir / "cx-o02-binary-copy.png",
                            [((1073, 18, 1720, 422), (30, 96))])]
    # Clip surrounding metadata from each line of the serialized metrics object.
    # Both strips use the SAME 2x affine transform: no token reflow,
    # joining of labels/values, or reconstruction of source UI text.
    metric_boxes = [(1288, 725, 1564, 741), (1262, 744, 1278, 758)]
    metric_crops = [(box, (709 + (box[0] - 1262) * 2,
                           174 + (box[1] - 725) * 2), 2) for box in metric_boxes]
    sources.append(paste_source(canvas, source_dir / "cx-o02-notebook-parse.png", [
        ((90, 835, 545, 867), (709, 96)),
        ((1255, 562, 1340, 588), (709, 140)),
        *metric_crops,
    ]))
    sources[-1]["crop_method"] = (
        "Serialized metrics object clipped line by line, retaining original relative "
        "positions and wrapping under a shared 2x NEAREST transform. Surrounding output metadata omitted; no token reflow "
        "or text reconstruction. Activity and Output heading are separate context crops."
    )
    sources[0]["heading"] = "Binary Copy file counts"
    sources[1]["heading"] = "Notebook row counts"
    for source, rectangle in zip(sources, cards):
        source["heading_y"] = rectangle[1] + style.PADDING
        source["card_rectangle"] = rectangle
    note = "Both Notebook row metrics reuse one parsed DataFrame count."
    style.label(canvas, (709, 258), note, style.NOTE_SIZE)
    save(canvas, "O02", "o02-file-vs-row-count.png", sources,
         "Binary Copy reports one file read and one written; the Notebook reports six "
         "source rows and six target rows. These are different measurement units.",
         ["Both Notebook row metrics reuse one parsed DataFrame count; no independent Bronze recount.",
          "End-to-end execution correlation is not independently verified.",
          "Separated UI crops omit operational/environment identifiers and intervening metadata.",
          "Metrics alone are enlarged 2x with NEAREST; original wrapping and relative positions retained."],
         title, [note])


if __name__ == "__main__":
    build_c12()
    build_o02()
