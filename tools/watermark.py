#!/usr/bin/env python3
"""Stamp job photos with a light Eamonn Lawlor watermark.

The mark is baked into the pixels: a small render of brand/logo-dark-bg.svg
(the PNG export sitting next to that SVG) plus the words "Eamonn Lawlor Paving",
bottom-right, at about 35% opacity, with a soft shadow.

The logo is drawn in white from the alpha of brand/logo-dark-bg.png, with
"Eamonn Lawlor Paving" in the bundled Inter SemiBold. The white mark is about
60% opacity, over a soft dark backing, about 22% of the image width, inset 3%.

Stamp clean photographs only. Files that already carry an elp-watermark marker
are skipped so a second run does not stamp on top of a stamp. Unwatermarked
originals of the first gallery stay in git history.

Examples:
  python3 tools/watermark.py
  python3 tools/watermark.py assets/img/gallery/resin-01-800.jpg
  python3 tools/watermark.py path/to/new-job.jpg --dest assets/img/gallery/new-800.jpg
"""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GALLERY = ROOT / "assets" / "img" / "gallery"
LOGO_PNG = ROOT / "brand" / "logo-dark-bg.png"
FONT_PATH = ROOT / "tools" / "fonts" / "Inter-SemiBold.ttf"
TEXT = "Eamonn Lawlor Paving"
MARKER = b"elp-watermark-v2"
WIDTH_FRACTION = 0.22
MARGIN_FRACTION = 0.03
OPACITY = 0.60


def find_font() -> Path:
    if FONT_PATH.is_file():
        return FONT_PATH
    raise SystemExit(f"Bundled font is missing: {FONT_PATH}")


def as_white(image: Image.Image) -> Image.Image:
    """Keep the logo shape, paint it white."""
    alpha = image.getchannel("A")
    white = Image.new("L", image.size, 255)
    return Image.merge("RGBA", (white, white, white, alpha))


def crop_to_alpha(image: Image.Image) -> Image.Image:
    band = image.getchannel("A") if "A" in image.getbands() else None
    if band is None:
        return image
    box = band.getbbox()
    if not box:
        return image
    return image.crop(box)


def render_lines(lines: list[str], font: ImageFont.FreeTypeFont) -> Image.Image:
    spacing = max(1, int(font.size * 0.12))
    boxes = [font.getbbox(line) for line in lines]
    widths = [box[2] - box[0] for box in boxes]
    heights = [box[3] - box[1] for box in boxes]
    width = max(widths) + 2
    height = sum(heights) + spacing * (len(lines) - 1) + 2
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    y = 0
    for line, box, line_height in zip(lines, boxes, heights):
        draw.text((-box[0] + 1, y - box[1] + 1), line, font=font, fill=(255, 255, 255, 255))
        y += line_height + spacing
    return canvas


def fit_font(text: str, max_width: int, font_path: Path) -> ImageFont.FreeTypeFont:
    low, high = 8, max(12, max_width)
    best = ImageFont.truetype(str(font_path), 8)
    while low <= high:
        size = (low + high) // 2
        font = ImageFont.truetype(str(font_path), size)
        box = font.getbbox(text)
        if box[2] - box[0] <= max_width:
            best = font
            low = size + 1
        else:
            high = size - 1
    return best


def build_mark(logo: Image.Image, target_width: int, font_path: Path) -> Image.Image:
    """Logo plus two lines of white text, about target_width pixels wide."""
    logo_width = max(18, int(target_width * 0.34))
    logo_height = max(18, int(logo_width * logo.height / logo.width))
    logo_small = as_white(logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS))
    text_width = max(24, target_width - logo_width - max(4, target_width // 18))
    font = fit_font("Eamonn Lawlor", text_width, font_path)
    text = render_lines(["Eamonn Lawlor", "Paving"], font)
    gap = max(4, target_width // 28)
    height = max(logo_small.height, text.height)
    mark = Image.new("RGBA", (logo_small.width + gap + text.width, height), (0, 0, 0, 0))
    mark.paste(logo_small, (0, (height - logo_small.height) // 2), logo_small)
    mark.paste(text, (logo_small.width + gap, (height - text.height) // 2), text)
    if mark.width > target_width and mark.width > 0:
        scale = target_width / mark.width
        mark = mark.resize((target_width, max(1, int(mark.height * scale))), Image.Resampling.LANCZOS)
    return mark


def with_opacity(image: Image.Image, opacity: float) -> Image.Image:
    red, green, blue, alpha = image.split()
    alpha = alpha.point(lambda value: int(value * opacity))
    return Image.merge("RGBA", (red, green, blue, alpha))


def dark_backing(mark: Image.Image) -> tuple[Image.Image, tuple[int, int]]:
    """Soft dark chip behind the white mark so it reads on light paving and grass."""
    pad = max(6, mark.width // 16)
    blur = max(2, mark.width // 30)
    width = mark.width + pad * 2 + blur * 2
    height = mark.height + pad * 2 + blur * 2
    plate = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(plate)
    radius = max(8, mark.height // 2)
    draw.rounded_rectangle(
        (blur, blur, width - blur - 1, height - blur - 1),
        radius=radius,
        fill=(0, 0, 0, 200),
    )
    plate = plate.filter(ImageFilter.GaussianBlur(blur))
    return plate, (blur + pad, blur + pad)


def stamp(image: Image.Image, logo: Image.Image, font_path: Path) -> Image.Image:
    base = image.convert("RGBA")
    target = max(96, int(round(base.width * WIDTH_FRACTION)))
    full = build_mark(logo, target, font_path)
    backing, offset = dark_backing(full)
    mark = with_opacity(full, OPACITY)
    margin = max(8, int(round(base.width * MARGIN_FRACTION)))
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    x = base.width - margin - offset[0] - mark.width
    y = base.height - margin - offset[1] - mark.height
    layer.paste(backing, (x - offset[0], y - offset[1]), backing)
    layer.paste(mark, (x, y), mark)
    return Image.alpha_composite(base, layer)


def already_stamped(image: Image.Image) -> bool:
    chunks = []
    for key in ("comment", "xmp", "exif"):
        value = image.info.get(key)
        if isinstance(value, str):
            value = value.encode()
        if isinstance(value, bytes):
            chunks.append(value)
    return b"elp-watermark" in b"".join(chunks)


def save_like(image: Image.Image, destination: Path, original_size: int) -> None:
    rgb = image.convert("RGB")
    suffix = destination.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        chosen = None
        for quality in (84, 80, 76, 72, 68, 64):
            buffer = io.BytesIO()
            rgb.save(buffer, "JPEG", quality=quality, optimize=True, comment=MARKER)
            payload = buffer.getvalue()
            chosen = payload
            if len(payload) <= int(original_size * 1.12):
                break
        destination.write_bytes(chosen)
        return
    if suffix == ".webp":
        chosen = None
        for quality in (78, 74, 70, 66, 62):
            buffer = io.BytesIO()
            rgb.save(buffer, "WEBP", quality=quality, method=6, xmp=MARKER)
            payload = buffer.getvalue()
            chosen = payload
            if len(payload) <= int(original_size * 1.12):
                break
        destination.write_bytes(chosen)
        return
    raise SystemExit(f"Unsupported image type: {destination}")


def gallery_files(folder: Path) -> list[Path]:
    files = []
    for path in sorted(folder.iterdir()):
        if path.suffix.lower() in {".jpg", ".jpeg", ".webp"} and path.is_file():
            files.append(path)
    return files


def stamp_file(path: Path, logo: Image.Image, font_path: Path, dest: Path | None = None) -> str:
    dest = dest or path
    with Image.open(path) as source:
        source.load()
        if already_stamped(source):
            return "skipped"
        original_size = path.stat().st_size
        stamped = stamp(source, logo, font_path)
    save_like(stamped, dest, original_size)
    return "stamped"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bake the Eamonn Lawlor watermark into job photos.")
    parser.add_argument("paths", nargs="*", help="Image files or a gallery directory. Defaults to assets/img/gallery/.")
    parser.add_argument("--dest", type=Path, help="Write a single input to this path instead of replacing it.")
    args = parser.parse_args(argv)

    if not LOGO_PNG.is_file():
        raise SystemExit(f"Missing rendered logo PNG: {LOGO_PNG}")
    logo = crop_to_alpha(Image.open(LOGO_PNG).convert("RGBA"))
    font_path = find_font()

    targets: list[Path]
    if not args.paths:
        targets = gallery_files(DEFAULT_GALLERY)
    else:
        targets = []
        for raw in args.paths:
            path = Path(raw)
            if path.is_dir():
                targets.extend(gallery_files(path))
            else:
                targets.append(path)
    if args.dest and len(targets) != 1:
        raise SystemExit("--dest can only be used with one input image.")

    stamped = skipped = 0
    for path in targets:
        result = stamp_file(path, logo, font_path, args.dest)
        if result == "stamped":
            stamped += 1
        else:
            skipped += 1
        print(f"{result}: {path}")
    print(f"Done. Stamped {stamped}, skipped {skipped}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
