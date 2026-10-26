"""Shared, restrained presentation for evidence composites.

Set EVIDENCE_FONT_PATH to use a specific local regular sans-serif font.
Reproducing a manifest byte-for-byte requires its recorded font hash and Pillow
version. Font files are not copied into the repository.
"""

import hashlib
import os
from functools import lru_cache
from pathlib import Path

from PIL import ImageDraw, ImageFont


BACKGROUND = "#f6f8fa"
PANEL = "#ffffff"
BORDER = "#d0d7de"
TEXT = "#24292f"
MUTED = "#57606a"
TITLE_SIZE = 26
HEADING_SIZE = 17
NOTE_SIZE = 16
MARGIN = 20
PADDING = 10
HEADING_HEIGHT = 22
FIRST_PANEL_Y = 64
GAP = 12


@lru_cache(maxsize=1)
def font_path():
    requested = os.environ.get("EVIDENCE_FONT_PATH")
    candidates = [requested] if requested else [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "Arial.ttf", "DejaVuSans.ttf", "NotoSans-Regular.ttf",
    ]
    for candidate in candidates:
        try:
            return Path(ImageFont.truetype(candidate, TITLE_SIZE).path)
        except OSError:
            continue
    raise ValueError("Set EVIDENCE_FONT_PATH to an available regular sans-serif font")


@lru_cache(maxsize=None)
def font(size):
    return ImageFont.truetype(str(font_path()), size)


def label(canvas, xy, value, size=HEADING_SIZE, color=MUTED):
    draw = ImageDraw.Draw(canvas)
    bounds = draw.textbbox(xy, value, font=font(size), anchor="lt")
    if (bounds[0] < 0 or bounds[1] < 0 or bounds[2] > canvas.width - MARGIN
            or bounds[3] > canvas.height - PADDING):
        raise ValueError("Label exceeds canvas bounds")
    draw.text(xy, value, font=font(size), fill=color, anchor="lt")


def card(canvas, rectangle, heading):
    x, y, width, height = rectangle
    ImageDraw.Draw(canvas).rounded_rectangle(
        (x, y, x + width - 1, y + height - 1),
        radius=4, fill=PANEL, outline=BORDER, width=1,
    )
    label(canvas, (x + PADDING, y + PADDING), heading)


def vertical_layout(sizes):
    panel_width = max(width for width, _ in sizes) + 2 * PADDING
    panels, cursor = [], FIRST_PANEL_Y
    for width, height in sizes:
        panel_height = 2 * PADDING + HEADING_HEIGHT + height
        panels.append({
            "card_rectangle": [MARGIN, cursor, panel_width, panel_height],
            "heading_y": cursor + PADDING,
            "rectangle": [MARGIN + PADDING, cursor + PADDING + HEADING_HEIGHT, width, height],
        })
        cursor += panel_height + GAP
    return panel_width + 2 * MARGIN, cursor - GAP + MARGIN, panels


def metadata():
    path = font_path()
    family, variant = font(TITLE_SIZE).getname()
    return {
        "canvas_color": BACKGROUND,
        "panel_color": PANEL,
        "border_color": BORDER,
        "border_width": 1,
        "corner_radius": 4,
        "title_size": TITLE_SIZE,
        "panel_heading_size": HEADING_SIZE,
        "note_size": NOTE_SIZE,
        "font": {"family": family, "style": variant, "file_name": path.name,
                 "sha256": hashlib.sha256(path.read_bytes()).hexdigest()},
        "margin": MARGIN,
        "panel_padding": PADDING,
        "panel_gap": GAP,
    }
