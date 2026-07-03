#!/usr/bin/env python3
"""Generate Questle Google Play listing assets into the Pages repo.

Set QUESTLE_APP_ROOT to the Flutter app checkout. The output PNGs are committed
to this Pages repo so questle.org can host/download the current listing assets.
"""

from __future__ import annotations

import os
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


PAGES_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = Path(os.environ.get("QUESTLE_APP_ROOT", PAGES_ROOT.parent / "questle-app"))
OUT = PAGES_ROOT / "assets" / "marketing" / "google-play"
SPRITES = APP_ROOT / "assets" / "sprites"
FONT = APP_ROOT / "assets" / "fonts" / "Sora[wght].ttf"

INK = "#171B2D"
MUTED = "#6C7080"
PRIMARY = "#6467D9"
PRIMARY_DEEP = "#343779"
PRIMARY_SOFT = "#E9EAFB"
ACCENT = "#F48B74"
ACCENT_SOFT = "#FFE9E3"
SUCCESS = "#7E927B"
SUCCESS_SOFT = "#E7EEE5"
INFO_SOFT = "#E6EFF6"
SURFACE = "#FFFFFF"
RAISED = "#F7F8FC"
BORDER = "#D9DBE6"


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT), size=size)


F = {
    "display": font(70),
    "h1": font(54),
    "h2": font(40),
    "h3": font(31),
    "body": font(25),
    "body_sm": font(21),
    "label": font(20),
    "tiny": font(16),
}


def rgb(size: tuple[int, int], color: str = SURFACE) -> Image.Image:
    return Image.new("RGB", size, color)


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    *,
    width: int,
    fill: str,
    font_obj: ImageFont.FreeTypeFont,
    line_gap: int = 8,
    max_lines: int | None = None,
) -> int:
    avg = max(font_obj.getlength("abcdefghijklmnopqrstuvwxyz") / 26, 1)
    chars = max(8, int(width / avg))
    lines: list[str] = []
    for part in text.split("\n"):
        lines.extend(wrap(part, chars) or [""])
    if max_lines is not None:
        lines = lines[:max_lines]
    x, y = xy
    for line in lines:
        draw.text((x, y), line, fill=fill, font=font_obj)
        box = draw.textbbox((x, y), line, font=font_obj)
        y += box[3] - box[1] + line_gap
    return y


def rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: str,
    outline: str | None = None,
    width: int = 2,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_center(
    draw: ImageDraw.ImageDraw,
    text: str,
    box: tuple[int, int, int, int],
    fill: str,
    font_obj: ImageFont.FreeTypeFont,
) -> None:
    tb = draw.textbbox((0, 0), text, font=font_obj)
    tw = tb[2] - tb[0]
    th = tb[3] - tb[1]
    x = box[0] + (box[2] - box[0] - tw) / 2
    y = box[1] + (box[3] - box[1] - th) / 2 - 2
    draw.text((x, y), text, fill=fill, font=font_obj)


def sprite(name: str) -> Image.Image:
    return Image.open(SPRITES / name).convert("RGBA")


def paste_fit(canvas: Image.Image, image: Image.Image, box: tuple[int, int, int, int]) -> None:
    bw = box[2] - box[0]
    bh = box[3] - box[1]
    iw, ih = image.size
    scale = min(bw / iw, bh / ih)
    nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
    resized = image.resize((nw, nh), Image.Resampling.LANCZOS)
    x = box[0] + (bw - nw) // 2
    y = box[1] + (bh - nh) // 2
    canvas.paste(resized, (x, y), resized)


def chip(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    *,
    fill: str = RAISED,
    color: str = MUTED,
) -> int:
    w = int(draw.textlength(text, font=F["label"])) + 44
    rounded(draw, (x, y, x + w, y + 50), 25, fill, BORDER, 2)
    text_center(draw, text, (x, y, x + w, y + 50), color, F["label"])
    return x + w + 12


def poster_base(title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = rgb((1080, 1920), SURFACE)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1080, 250), fill=PRIMARY_SOFT)
    draw.text((64, 56), title, fill=INK, font=F["h1"])
    draw_wrapped(draw, subtitle, (66, 128), width=830, fill=MUTED, font_obj=F["body"], max_lines=2)
    return img, draw


def bottom_nav(draw: ImageDraw.ImageDraw, y: int = 1768) -> None:
    rounded(draw, (72, y, 1008, y + 96), 48, SURFACE, BORDER, 2)
    items = [("Home", PRIMARY), ("Trail", MUTED), ("Create", MUTED), ("Badges", MUTED), ("Profile", MUTED)]
    for i, (label, color) in enumerate(items):
        x = 132 + i * 184
        draw.ellipse((x, y + 23, x + 20, y + 43), fill=color)
        text_center(draw, label, (x - 58, y + 45, x + 78, y + 84), color, F["tiny"])


def home_screen() -> Image.Image:
    img, draw = poster_base("Browse tiny solo quests", "Pick by mood, place, and energy. Questle keeps the day light.")
    paste_fit(img, sprite("quest.png"), (770, 56, 990, 230))
    rounded(draw, (54, 310, 1026, 860), 52, SURFACE, PRIMARY_SOFT, 5)
    draw.text((108, 380), "Today's Questle", fill=PRIMARY_DEEP, font=F["h3"])
    chip(draw, 405, 372, "EASY", fill=SUCCESS_SOFT, color=SUCCESS)
    draw.text((108, 446), "Take yourself out\nfor coffee", fill=INK, font=F["display"])
    draw_wrapped(draw, "Go to a cafe or coffee stand, order one drink, and settle into the moment.", (108, 630), width=580, fill=MUTED, font_obj=F["body"])
    paste_fit(img, sprite("category_cafe.png"), (690, 395, 975, 680))
    rounded(draw, (108, 742, 512, 814), 36, INK)
    text_center(draw, "Complete Quest", (108, 742, 512, 814), SURFACE, F["label"])
    chip(draw, 536, 754, "Reroll")
    chip(draw, 710, 754, "Lock")
    draw.line((80, 928, 1000, 928), fill=BORDER, width=3)
    draw.text((78, 980), "Choose from the catalog", fill=INK, font=F["h2"])
    x = 78
    for label, selected in [("All", True), ("Creative", False), ("Explore", False), ("Cafe", False)]:
        x = chip(draw, x, 1048, label, fill=PRIMARY if selected else SURFACE, color=SURFACE if selected else MUTED)
    cards = [
        ("Make a tiny sketch", "Creative", "20m", "category_creative.png"),
        ("Field trip nearby", "Explore", "15m", "category_explore.png"),
    ]
    for i, (title, cat, dur, art) in enumerate(cards):
        left = 78 + i * 474
        rounded(draw, (left, 1140, left + 414, 1668), 42, SURFACE, BORDER, 2)
        paste_fit(img, sprite(art), (left + 76, 1180, left + 338, 1428))
        draw_wrapped(draw, title, (left + 42, 1450), width=320, fill=INK, font_obj=F["h3"], line_gap=5, max_lines=2)
        draw.text((left + 42, 1538), cat, fill=PRIMARY, font=F["label"])
        chip(draw, left + 42, 1588, dur)
        chip(draw, left + 178, 1588, "Easy")
    bottom_nav(draw)
    return img


def detail_screen() -> Image.Image:
    img, draw = poster_base("Know what you're starting", "Open a quest, scan the steps, then start when it feels right.")
    rounded(draw, (64, 312, 1016, 1718), 52, SURFACE, BORDER, 2)
    rounded(draw, (114, 360, 966, 862), 44, RAISED, BORDER, 2)
    paste_fit(img, sprite("category_explore.png"), (265, 384, 815, 832))
    draw_wrapped(draw, "Do a convenience store field trip", (114, 930), width=810, fill=INK, font_obj=F["h1"], line_gap=5, max_lines=2)
    x = 114
    for label in ["Explore", "15m", "Easy", "Nearby"]:
        x = chip(draw, x, 1080, label, fill=PRIMARY_SOFT if label == "Explore" else RAISED, color=PRIMARY_DEEP if label == "Explore" else MUTED)
    draw.text((114, 1178), "How to do it", fill=INK, font=F["h3"])
    draw_wrapped(draw, "Walk the aisles slowly. Pick one small item you have never tried, then notice what caught your eye.", (114, 1230), width=800, fill=MUTED, font_obj=F["body"])
    draw.text((114, 1386), "Why this quest", fill=INK, font=F["h3"])
    draw_wrapped(draw, "A tiny errand can become a low-pressure reset when it has a little curiosity built in.", (114, 1438), width=800, fill=MUTED, font_obj=F["body"])
    rounded(draw, (114, 1598, 966, 1678), 40, INK)
    text_center(draw, "Start Quest", (114, 1598, 966, 1678), SURFACE, F["label"])
    return img


def trail_screen() -> Image.Image:
    img, draw = poster_base("Save your Questle trail", "Notes, moods, photos, and dates become a private memory map.")
    paste_fit(img, sprite("intro_trail.png"), (710, 70, 1018, 300))
    draw.text((72, 330), "Quest Trail", fill=INK, font=F["h1"])
    draw.text((74, 402), "Your solo memories over time.", fill=MUTED, font=F["body"])
    rounded(draw, (54, 492, 1026, 920), 44, SURFACE, BORDER, 2)
    draw.text((92, 540), "July 2026", fill=INK, font=F["h2"])
    for i, day in enumerate(["M", "T", "W", "T", "F", "S", "S"]):
        text_center(draw, day, (104 + i * 126, 620, 164 + i * 126, 660), MUTED, F["label"])
    n = 1
    for row in range(4):
        for col in range(7):
            cx = 132 + col * 126
            cy = 710 + row * 72
            fill = PRIMARY_SOFT if n in [3, 9, 18] else SURFACE
            outline = PRIMARY if n in [3, 9, 18] else BORDER
            draw.ellipse((cx - 27, cy - 27, cx + 27, cy + 27), fill=fill, outline=outline, width=2)
            text_center(draw, str(n), (cx - 27, cy - 27, cx + 27, cy + 27), PRIMARY_DEEP if n in [3, 9, 18] else MUTED, F["tiny"])
            n += 1
    draw.text((72, 996), "Timeline", fill=INK, font=F["h2"])
    y = 1060
    for title, meta, date in [
        ("Take yourself out for coffee", "Calm note - no photo", "Today"),
        ("Make a tiny sketch", "Creative memory - photo", "Yesterday"),
        ("Sit outside five minutes", "Mood saved", "Mon"),
    ]:
        rounded(draw, (72, y, 1008, y + 160), 34, SURFACE, BORDER, 2)
        draw.text((112, y + 32), title, fill=INK, font=F["h3"])
        draw.text((112, y + 88), meta, fill=MUTED, font=F["body_sm"])
        text_center(draw, date, (826, y + 48, 962, y + 106), PRIMARY_DEEP, F["label"])
        y += 188
    bottom_nav(draw)
    return img


def badges_screen() -> Image.Image:
    img, draw = poster_base("Collect quiet wins", "Badges mark the story without turning it into a public feed.")
    draw.text((72, 330), "Questle Badges", fill=INK, font=F["h1"])
    draw.text((74, 402), "Stamps for small steps and steady rituals.", fill=MUTED, font=F["body"])
    arts = ["badge.png", "category_cafe.png", "category_creative.png", "category_nature.png", "category_reflection.png", "category_explore.png"]
    labels = ["First Step", "Cafe Quest", "Maker", "Fresh Air", "Reflector", "Explorer"]
    for i, (art, label) in enumerate(zip(arts, labels)):
        col = i % 2
        row = i // 2
        left = 72 + col * 480
        top = 510 + row * 385
        rounded(draw, (left, top, left + 432, top + 330), 40, SURFACE, BORDER, 2)
        rounded(draw, (left + 84, top + 28, left + 348, top + 222), 34, RAISED, BORDER, 2)
        paste_fit(img, sprite(art), (left + 120, top + 36, left + 312, top + 214))
        draw.text((left + 42, top + 246), label, fill=INK, font=F["h3"])
        draw.text((left + 42, top + 292), "Earned quietly", fill=MUTED, font=F["body_sm"])
    bottom_nav(draw)
    return img


def profile_screen() -> Image.Image:
    img, draw = poster_base("Make Questle yours", "Custom quests, richer memories, and backup are ready when you are.")
    rounded(draw, (64, 316, 1016, 600), 48, SURFACE, BORDER, 2)
    paste_fit(img, sprite("profile_cat_table.png"), (88, 348, 300, 560))
    draw.text((332, 374), "Questle Explorer", fill=INK, font=F["h2"])
    draw.text((334, 432), "Private progress, saved locally.", fill=MUTED, font=F["body"])
    for i, (v, label) in enumerate([("7", "Streak"), ("18", "Done"), ("9", "Memories"), ("6", "Badges")]):
        x = 334 + i * 154
        draw.text((x, 505), v, fill=PRIMARY_DEEP, font=F["h3"])
        draw.text((x, 548), label, fill=MUTED, font=F["tiny"])
    rounded(draw, (64, 672, 1016, 1082), 46, PRIMARY_DEEP)
    draw.text((116, 732), "Questle Pro", fill=SURFACE, font=F["h2"])
    draw_wrapped(draw, "Unlimited catalog picks, more custom Questles, photo memories, and progress backup.", (116, 794), width=760, fill="#F7F8FC", font_obj=F["body"])
    rounded(draw, (116, 958, 522, 1030), 36, ACCENT)
    text_center(draw, "Unlock Pro", (116, 958, 522, 1030), SURFACE, F["label"])
    paste_fit(img, sprite("intro_memories.png"), (700, 752, 960, 1012))
    rounded(draw, (64, 1168, 1016, 1452), 44, SURFACE, BORDER, 2)
    draw.text((116, 1228), "Account Backup", fill=INK, font=F["h2"])
    draw_wrapped(draw, "Sign in with Google to prepare progress backup across devices. Photo memories stay on this device.", (116, 1292), width=790, fill=MUTED, font_obj=F["body"])
    rounded(draw, (116, 1380, 458, 1432), 26, PRIMARY_SOFT, BORDER)
    text_center(draw, "Google sign-in", (116, 1380, 458, 1432), PRIMARY_DEEP, F["label"])
    bottom_nav(draw)
    return img


def intro_screen() -> Image.Image:
    img, draw = poster_base("A calm start, not a feed", "Solo prompts, private memories, and gentle momentum.")
    y = 330
    for title, art in [
        ("Discover solo quests", "intro_discover.png"),
        ("Choose by mood", "intro_choose.png"),
        ("Save memories", "intro_memories.png"),
        ("Grow your trail", "intro_trail.png"),
    ]:
        rounded(draw, (72, y, 1008, y + 310), 42, SURFACE, BORDER, 2)
        paste_fit(img, sprite(art), (104, y + 28, 360, y + 278))
        draw.text((400, y + 82), title, fill=INK, font=F["h2"])
        draw_wrapped(draw, "A premium onboarding rhythm with simple art and no noisy dashboard.", (402, y + 144), width=500, fill=MUTED, font_obj=F["body_sm"])
        y += 350
    rounded(draw, (176, 1694, 904, 1768), 37, INK)
    text_center(draw, "Start exploring", (176, 1694, 904, 1768), SURFACE, F["label"])
    return img


def feature_graphic() -> Image.Image:
    img = rgb((1024, 500), PRIMARY_SOFT)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((650, -90, 1120, 600), radius=180, fill=INFO_SOFT)
    draw.rounded_rectangle((-110, 310, 410, 610), radius=150, fill=ACCENT_SOFT)
    paste_fit(img, sprite("quest.png"), (575, 82, 780, 292))
    paste_fit(img, sprite("cafe.png"), (750, 130, 990, 390))
    paste_fit(img, sprite("badge.png"), (560, 300, 700, 440))
    draw.text((70, 74), "Questle", fill=PRIMARY_DEEP, font=font(58))
    draw_wrapped(draw, "Small solo quests for ordinary days.", (72, 150), width=440, fill=INK, font_obj=font(42), line_gap=8, max_lines=2)
    draw_wrapped(draw, "Browse a tiny quest, complete it, and keep a private trail of memories.", (74, 282), width=430, fill=MUTED, font_obj=font(22), line_gap=6, max_lines=3)
    rounded(draw, (74, 390, 316, 454), 32, INK)
    text_center(draw, "Solo quest catalog", (74, 390, 316, 454), SURFACE, font(16))
    rounded(draw, (336, 390, 504, 454), 32, SURFACE, BORDER, 2)
    text_center(draw, "Local-first", (336, 390, 504, 454), PRIMARY_DEEP, font(16))
    return img


def export() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assets = {
        "feature-graphic-1024x500.png": feature_graphic(),
        "phone-01-home-catalog-1080x1920.png": home_screen(),
        "phone-02-quest-detail-1080x1920.png": detail_screen(),
        "phone-03-quest-trail-1080x1920.png": trail_screen(),
        "phone-04-badges-1080x1920.png": badges_screen(),
        "phone-05-profile-pro-backup-1080x1920.png": profile_screen(),
        "phone-06-feature-intro-1080x1920.png": intro_screen(),
    }
    for name, image in assets.items():
        image.convert("RGB").save(OUT / name, optimize=True)

    sprite("app_icon.png").resize((512, 512), Image.Resampling.LANCZOS).save(
        OUT / "app-icon-512.png",
        optimize=True,
    )

    (OUT / "listing-copy.md").write_text(
        "\n".join(
            [
                "# Questle Google Play Listing Copy",
                "",
                "Short description: Tiny solo quests, private memories, and calm progress for ordinary days.",
                "",
                "Screenshot alt text:",
                "1. Home catalog showing Today's Questle, quest categories, and browseable solo quest cards.",
                "2. Quest detail screen showing how-to guidance and a Start Quest action.",
                "3. Quest Trail calendar and timeline with saved memories.",
                "4. Questle Badges collection grid with earned stamps.",
                "5. Profile screen with Pro benefits and Account Backup.",
                "6. Feature intro panels for discovery, mood choice, memories, and trail growth.",
                "",
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    export()
