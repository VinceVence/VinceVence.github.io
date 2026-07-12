#!/usr/bin/env python3
"""Build Guwa website review, social, and generated-asset metadata."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "assets" / "guwa-site"
OPTIMIZED = GENERATED / "optimized"
PREVIEW = ROOT / "docs" / "website" / "preview"
BRAND = ROOT / "assets" / "brand"
ILLUSTRATIONS = ROOT / "assets" / "illustrations"
FONT_PATH = ROOT / "assets" / "fonts" / "Sora.ttf"

INK = "#171B2D"
DEEP = "#343779"
PRIMARY = "#6467D9"
LAVENDER = "#E9EAFB"
CORAL = "#F48B74"
GOLD = "#D9A64E"
WHITE = "#FFFFFF"

ASSETS = [
    {
        "slug": "guwa-hero-doorway",
        "concept": "Hero doorway",
        "section": "Hero",
        "references": ["intro_discover.png", "intro_trail.png", "guwa_mark_transparent.png"],
        "alt": "Guwa cat stepping through an open doorway to begin a small adventure.",
    },
    {
        "slug": "guwa-find-activity",
        "concept": "Find an activity",
        "section": "How Guwa works",
        "references": ["intro_choose.png", "profile_cat_table.png", "guwa_mark_transparent.png"],
        "alt": "Guwa cat choosing between three simple activity prompts.",
    },
    {
        "slug": "guwa-go-experience",
        "concept": "Go experience it",
        "section": "How Guwa works",
        "references": ["intro_discover.png", "intro_trail.png", "quest.png"],
        "alt": "Guwa cat following a short curved trail toward a small flag.",
    },
    {
        "slug": "guwa-keep-memory",
        "concept": "Keep the memory",
        "section": "Memories",
        "references": ["intro_memories.png", "profile_cat_table.png", "intro_trail.png"],
        "alt": "Guwa cat beside a notebook, photo frame, mood mark, and calendar.",
    },
    {
        "slug": "guwa-progress-badges",
        "concept": "Progress your way",
        "section": "Progress",
        "references": ["intro_trail.png", "badge.png", "home_greeting.png"],
        "alt": "Guwa cat placing a badge on a short personal progress trail.",
    },
    {
        "slug": "guwa-founder-pass",
        "concept": "Founder Pass",
        "section": "Founder Pass",
        "references": ["home_greeting.png", "profile_cat_table.png", "badge.png"],
        "alt": "Guwa cat presenting a blank golden Founder Pass ticket.",
    },
]


def font(size: int, weight: int = 600) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_PATH), size=size, layout_engine=ImageFont.Layout.RAQM)


def contain(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    copy = image.copy()
    copy.thumbnail(size, Image.Resampling.LANCZOS)
    return copy


def paste_center(canvas: Image.Image, image: Image.Image, box: tuple[int, int, int, int]) -> None:
    left, top, right, bottom = box
    fitted = contain(image, (right - left, bottom - top))
    x = left + (right - left - fitted.width) // 2
    y = top + (bottom - top - fitted.height) // 2
    canvas.alpha_composite(fitted, (x, y))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_review_sheet() -> None:
    PREVIEW.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGBA", (2400, 2700), WHITE)
    draw = ImageDraw.Draw(canvas)
    draw.text((120, 90), "Guwa website illustration review", font=font(72, 800), fill=INK)
    draw.text(
        (120, 190),
        "Six marketing-only concepts derived from production sprites. No app art is replaced.",
        font=font(30),
        fill=DEEP,
    )

    for index, item in enumerate(ASSETS):
        column = index % 2
        row = index // 2
        x = 80 + column * 1160
        y = 310 + row * 780
        draw.rounded_rectangle((x, y, x + 1080, y + 700), radius=42, fill=WHITE, outline=LAVENDER, width=5)
        draw.text((x + 48, y + 38), item["concept"], font=font(38, 800), fill=INK)
        draw.text((x + 48, y + 94), f"Section: {item['section']}", font=font(22, 700), fill=PRIMARY)

        art = Image.open(OPTIMIZED / f"{item['slug']}-master.png").convert("RGBA")
        light_box = (x + 48, y + 150, x + 718, y + 545)
        dark_box = (x + 746, y + 150, x + 1032, y + 545)
        draw.rounded_rectangle(light_box, radius=28, fill=LAVENDER)
        draw.rounded_rectangle(dark_box, radius=28, fill=DEEP)
        paste_center(canvas, art, (light_box[0] + 20, light_box[1] + 20, light_box[2] - 20, light_box[3] - 20))
        paste_center(canvas, art, (dark_box[0] + 20, dark_box[1] + 28, dark_box[2] - 20, dark_box[3] - 28))
        draw.text((x + 48, y + 565), "Desktop / light", font=font(20, 700), fill=INK)
        draw.text((x + 746, y + 565), "Mobile / purple", font=font(20, 700), fill=INK)
        refs = "References: " + ", ".join(item["references"])
        draw.text((x + 48, y + 620), refs, font=font(16), fill=DEEP)

    canvas.convert("RGB").save(PREVIEW / "guwa-imagegen-review.png", optimize=True)


def build_open_graph() -> None:
    canvas = Image.new("RGBA", (1200, 630), DEEP)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((650, 55, 1145, 575), radius=56, fill=LAVENDER)
    art = Image.open(OPTIMIZED / "guwa-hero-doorway-master.png").convert("RGBA")
    paste_center(canvas, art, (690, 85, 1110, 545))
    wordmark = Image.open(BRAND / "guwa-wordmark-light.png").convert("RGBA")
    wordmark = contain(wordmark, (240, 90))
    canvas.alpha_composite(wordmark, (80, 70))
    draw.text((80, 210), "Small adventures", font=font(62, 800), fill=WHITE)
    draw.text((80, 286), "for ordinary days.", font=font(62, 800), fill=WHITE)
    draw.rectangle((80, 405, 160, 413), fill=GOLD)
    draw.text((80, 445), "Find something. Go do it. Keep the memory.", font=font(25, 600), fill=LAVENDER)
    canvas.convert("RGB").save(BRAND / "guwa-open-graph-1200x630.png", optimize=True)


def build_feature_graphic() -> None:
    canvas = Image.new("RGBA", (1024, 500), LAVENDER)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 18, 500), fill=PRIMARY)
    wordmark = Image.open(BRAND / "guwa-wordmark.png").convert("RGBA")
    wordmark = contain(wordmark, (280, 110))
    canvas.alpha_composite(wordmark, (70, 68))
    draw.text((70, 230), "Small adventures", font=font(48, 800), fill=INK)
    draw.text((70, 292), "for ordinary days.", font=font(48, 800), fill=INK)
    draw.rectangle((70, 390, 145, 398), fill=CORAL)
    sprite = Image.open(ILLUSTRATIONS / "guwa-home-greeting.png").convert("RGBA")
    paste_center(canvas, sprite, (590, 35, 990, 465))
    canvas.convert("RGB").save(BRAND / "guwa-website-feature-1024x500.png", optimize=True)


def build_manifest() -> None:
    records = []
    for item in ASSETS:
        source = GENERATED / "source" / f"{item['slug']}-source.png"
        master = OPTIMIZED / f"{item['slug']}-master.png"
        with Image.open(source) as image:
            source_size = list(image.size)
        derivatives = []
        for path in sorted(OPTIMIZED.glob(f"{item['slug']}-*")):
            with Image.open(path) as image:
                dimensions = list(image.size)
            derivatives.append(
                {
                    "filename": path.relative_to(ROOT).as_posix(),
                    "dimensions": dimensions,
                    "format": path.suffix.lstrip(".").upper(),
                    "sha256": sha256(path),
                }
            )
        records.append(
            {
                "filename": source.relative_to(ROOT).as_posix(),
                "concept": item["concept"],
                "sourceReferences": item["references"],
                "dimensions": source_size,
                "format": "PNG",
                "sha256": sha256(source),
                "websiteSection": item["section"],
                "altTextRecommendation": item["alt"],
                "transparentMaster": master.relative_to(ROOT).as_posix(),
                "derivatives": derivatives,
            }
        )
    output = GENERATED / "guwa-generated-assets.json"
    output.write_text(json.dumps({"palette": [PRIMARY, DEEP, LAVENDER, CORAL, GOLD, INK, WHITE], "assets": records}, indent=2) + "\n")


def main() -> None:
    build_review_sheet()
    build_open_graph()
    build_feature_graphic()
    build_manifest()


if __name__ == "__main__":
    main()
