#!/usr/bin/env python3
"""Generate Questle Google Play listing assets from the app's UI language."""

from __future__ import annotations

import os
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = Path(os.environ.get("QUESTLE_APP_ROOT", ROOT.parent / "questle-app"))
OUT = ROOT / "assets" / "marketing" / "google-play"
SPRITES = APP_ROOT / "assets" / "sprites"
FONT = APP_ROOT / "assets" / "fonts" / "Sora[wght].ttf"

INK = "#171B2D"
MUTED = "#6C7080"
QUIET = "#858A9B"
PRIMARY = "#6467D9"
PRIMARY_DEEP = "#343779"
PRIMARY_SOFT = "#E8E7FF"
PRIMARY_LINE = "#C8C5F7"
ACCENT = "#F48B74"
SUCCESS = "#52664F"
SUCCESS_SOFT = "#E8F0E6"
SURFACE = "#FFFFFF"
RAISED = "#F7F8FC"
BORDER = "#DCDDE6"
PHONE = (1080, 1920)


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT), size=size)


F = {
    "brand": font(34),
    "hero": font(64),
    "h1": font(58),
    "h2": font(42),
    "h3": font(32),
    "body": font(26),
    "body_sm": font(22),
    "label": font(21),
    "tiny": font(16),
}


def rgb(size: tuple[int, int], color: str = SURFACE) -> Image.Image:
    return Image.new("RGB", size, color)


def sprite(name: str) -> Image.Image:
    return Image.open(SPRITES / name).convert("RGBA")


def paste_fit(canvas: Image.Image, image: Image.Image, box: tuple[int, int, int, int], opacity: float = 1.0) -> None:
    bw = box[2] - box[0]
    bh = box[3] - box[1]
    iw, ih = image.size
    scale = min(bw / iw, bh / ih)
    resized = image.resize((max(1, int(iw * scale)), max(1, int(ih * scale))), Image.Resampling.LANCZOS)
    if opacity < 1:
        resized = resized.copy()
        resized.putalpha(resized.getchannel("A").point(lambda p: int(p * opacity)))
    x = box[0] + (bw - resized.width) // 2
    y = box[1] + (bh - resized.height) // 2
    canvas.paste(resized, (x, y), resized)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: str, outline: str | None = None, width: int = 2) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_center(draw: ImageDraw.ImageDraw, text: str, box: tuple[int, int, int, int], fill: str, fnt: ImageFont.FreeTypeFont) -> None:
    tb = draw.textbbox((0, 0), text, font=fnt)
    x = box[0] + (box[2] - box[0] - tb[2] + tb[0]) / 2
    y = box[1] + (box[3] - box[1] - tb[3] + tb[1]) / 2 - 1
    draw.text((x, y), text, fill=fill, font=fnt)


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], *, width: int, fill: str, fnt: ImageFont.FreeTypeFont, line_gap: int = 8, max_lines: int | None = None) -> int:
    chars = max(8, int(width / max(fnt.getlength("abcdefghijklmnopqrstuvwxyz") / 26, 1)))
    lines: list[str] = []
    for part in text.split("\n"):
        lines.extend(wrap(part, chars) or [""])
    if max_lines is not None:
        lines = lines[:max_lines]
    x, y = xy
    for line in lines:
        draw.text((x, y), line, fill=fill, font=fnt)
        box = draw.textbbox((x, y), line, font=fnt)
        y += box[3] - box[1] + line_gap
    return y


def chip(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, *, fill: str = SURFACE, color: str = MUTED, outline: str = BORDER, height: int = 56, pad: int = 28) -> int:
    w = int(draw.textlength(text, font=F["label"])) + pad * 2
    rounded(draw, (x, y, x + w, y + height), height // 2, fill, outline, 2)
    text_center(draw, text, (x, y, x + w, y + height), color, F["label"])
    return x + w + 12


def button(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, *, fill: str = INK, color: str = SURFACE, outline: str | None = None) -> None:
    rounded(draw, box, (box[3] - box[1]) // 2, fill, outline, 2)
    text_center(draw, label, box, color, F["label"])


def base() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = rgb(PHONE)
    draw = ImageDraw.Draw(img)
    draw.text((64, 36), "9:41", fill=INK, font=F["label"])
    draw.rounded_rectangle((884, 42, 936, 52), radius=5, fill=INK)
    draw.rounded_rectangle((944, 36, 1004, 56), radius=8, outline=INK, width=3)
    draw.rectangle((1008, 43, 1014, 49), fill=INK)
    draw.rounded_rectangle((950, 42, 984, 50), radius=4, fill=INK)
    return img, draw


def brand(img: Image.Image, draw: ImageDraw.ImageDraw, y: int = 90) -> None:
    paste_fit(img, sprite("logo.png"), (64, y, 122, y + 58))
    draw.text((136, y + 7), "Questle", fill=PRIMARY, font=F["brand"])


def nav(draw: ImageDraw.ImageDraw, active: str) -> None:
    y = 1782
    rounded(draw, (58, y, 1022, y + 98), 49, SURFACE, BORDER, 2)
    for i, label in enumerate(["Home", "Trail", "Create", "Badges", "Profile"]):
        cx = 122 + i * 209
        color = PRIMARY if label == active else QUIET
        if label == active:
            rounded(draw, (cx - 56, y + 18, cx + 56, y + 76), 29, PRIMARY_SOFT)
        draw.ellipse((cx - 10, y + 30, cx + 10, y + 50), fill=color)
        text_center(draw, label, (cx - 58, y + 53, cx + 58, y + 86), color, F["tiny"])


def quest_card(img: Image.Image, draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], art: str, title: str, category: str, minutes: str) -> None:
    rounded(draw, box, 38, SURFACE, BORDER, 2)
    x1, y1, x2, y2 = box
    paste_fit(img, sprite(art), (x1 + 74, y1 + 10, x2 - 74, y1 + 142))
    draw.text((x1 + 34, y1 + 158), category, fill=PRIMARY, font=F["label"])
    draw_wrapped(draw, title, (x1 + 34, y1 + 194), width=x2 - x1 - 68, fill=INK, fnt=F["body"], max_lines=2)
    chip(draw, x1 + 34, y2 - 50, minutes, fill=RAISED, height=42, pad=20)
    chip(draw, x1 + 148, y2 - 50, "Easy", fill=RAISED, height=42, pad=20)


def home_screen() -> Image.Image:
    img, draw = base()
    brand(img, draw)
    draw_wrapped(draw, "Ready for a tiny quest?", (64, 214), width=460, fill=INK, fnt=F["hero"], line_gap=0, max_lines=3)
    draw_wrapped(draw, "Choose one that fits your mood today.", (66, 426), width=430, fill=MUTED, fnt=F["body"], max_lines=2)
    paste_fit(img, sprite("home_greeting.png"), (552, 164, 1014, 474))
    rounded(draw, (54, 558, 1026, 1076), 54, SURFACE, PRIMARY_LINE, 4)
    draw.text((106, 620), "Today's Questle", fill=PRIMARY_DEEP, font=F["h3"])
    chip(draw, 388, 608, "EASY", fill=SUCCESS_SOFT, color=SUCCESS, outline=SUCCESS_SOFT, height=54)
    draw_wrapped(draw, "Take yourself out for coffee", (106, 704), width=590, fill=INK, fnt=F["h1"], line_gap=0, max_lines=2)
    draw_wrapped(draw, "Go to a cafe or coffee stand, order one drink, and settle into the moment.", (106, 870), width=704, fill=MUTED, fnt=F["body"], max_lines=2)
    paste_fit(img, sprite("category_cafe.png"), (724, 638, 984, 842))
    button(draw, (106, 980, 474, 1050), "Complete Quest")
    button(draw, (502, 980, 690, 1050), "Reroll", fill=SURFACE, color=PRIMARY_DEEP, outline=BORDER)
    button(draw, (714, 980, 894, 1050), "Lock", fill=SURFACE, color=PRIMARY_DEEP, outline=BORDER)
    draw.line((64, 1128, 1016, 1128), fill=BORDER, width=3)
    draw.text((64, 1186), "Choose from catalog", fill=INK, font=F["h2"])
    chip(draw, 682, 1178, "What are these?", fill=PRIMARY_SOFT, color=PRIMARY_DEEP, outline=PRIMARY_LINE)
    x = 64
    for label, active in [("All", True), ("Creative", False), ("Explore", False), ("Cafe", False)]:
        x = chip(draw, x, 1264, label, fill=PRIMARY_DEEP if active else SURFACE, color=SURFACE if active else MUTED, outline=PRIMARY_DEEP if active else BORDER, height=62, pad=34)
    draw.text((64, 1380), "1/1 catalog pick left this week", fill=MUTED, font=F["body_sm"])
    quest_card(img, draw, (64, 1444, 506, 1740), "category_creative.png", "Tiny sketch", "Creative", "20m")
    quest_card(img, draw, (542, 1444, 984, 1740), "category_explore.png", "Field trip nearby", "Explore", "15m")
    nav(draw, "Home")
    return img


def detail_screen() -> Image.Image:
    img, draw = base()
    draw.text((64, 106), "Quest detail", fill=INK, font=F["h2"])
    button(draw, (870, 92, 1004, 150), "Done", fill=SURFACE, color=PRIMARY_DEEP, outline=BORDER)
    paste_fit(img, sprite("category_explore.png"), (214, 196, 866, 652))
    draw_wrapped(draw, "Do a convenience store field trip", (64, 718), width=910, fill=INK, fnt=F["h1"], line_gap=0, max_lines=2)
    x = 64
    for label, active in [("Explore", True), ("15m", False), ("Easy", False), ("Nearby", False)]:
        x = chip(draw, x, 884, label, fill=PRIMARY_SOFT if active else RAISED, color=PRIMARY_DEEP if active else MUTED, outline=PRIMARY_LINE if active else BORDER)
    draw_wrapped(draw, "Make a tiny errand feel intentional. Walk slowly, pick one unfamiliar snack or drink, and notice what pulled your attention.", (64, 1002), width=884, fill=MUTED, fnt=F["body"], max_lines=4)
    draw.line((64, 1188, 1016, 1188), fill=BORDER, width=3)
    draw.text((64, 1246), "How to do it", fill=INK, font=F["h3"])
    for i, step in enumerate(["Wander one aisle you usually skip.", "Choose one small thing you have never tried.", "Take a short note before you head home."]):
        y = 1310 + i * 74
        rounded(draw, (64, y, 110, y + 46), 23, PRIMARY_SOFT)
        text_center(draw, str(i + 1), (64, y, 110, y + 46), PRIMARY_DEEP, F["label"])
        draw_wrapped(draw, step, (134, y + 4), width=786, fill=MUTED, fnt=F["body_sm"], max_lines=1)
    draw.text((64, 1548), "Why this quest", fill=INK, font=F["h3"])
    draw_wrapped(draw, "Curiosity changes the texture of an ordinary place without asking for a huge plan.", (64, 1600), width=880, fill=MUTED, fnt=F["body_sm"], max_lines=2)
    button(draw, (64, 1742, 728, 1822), "Start Quest")
    button(draw, (754, 1742, 1016, 1822), "Lock", fill=SURFACE, color=PRIMARY_DEEP, outline=BORDER)
    return img


def trail_screen() -> Image.Image:
    img, draw = base()
    draw.text((64, 116), "Quest Trail", fill=INK, font=F["h1"])
    draw.text((66, 188), "Your solo memories over time.", fill=MUTED, font=F["body"])
    paste_fit(img, sprite("intro_trail.png"), (712, 74, 1012, 274))
    rounded(draw, (54, 318, 1026, 832), 44, SURFACE, BORDER, 2)
    draw.text((100, 372), "July 2026", fill=INK, font=F["h2"])
    for i, day in enumerate(["M", "T", "W", "T", "F", "S", "S"]):
        text_center(draw, day, (118 + i * 122, 458, 178 + i * 122, 498), MUTED, F["label"])
    n = 1
    for row in range(5):
        for col in range(7):
            if n > 31:
                break
            cx, cy = 148 + col * 122, 566 + row * 64
            active = n in [3, 8, 14, 21]
            draw.ellipse((cx - 26, cy - 26, cx + 26, cy + 26), fill=PRIMARY_SOFT if active else SURFACE, outline=PRIMARY_LINE if active else BORDER, width=2)
            text_center(draw, str(n), (cx - 26, cy - 26, cx + 26, cy + 26), PRIMARY_DEEP if active else MUTED, F["tiny"])
            n += 1
    draw.text((64, 922), "Memory ledger", fill=INK, font=F["h2"])
    y = 994
    for title, meta, date in [("Take yourself out for coffee", "Calm note saved", "Today"), ("Make a tiny sketch", "Photo memory", "Yesterday"), ("Sit outside five minutes", "Mood saved", "Mon"), ("Visit a new shelf", "Culture quest", "Fri")]:
        draw.line((64, y, 1016, y), fill=BORDER, width=2)
        draw.text((64, y + 34), title, fill=INK, font=F["h3"])
        draw.text((64, y + 88), meta, fill=MUTED, font=F["body_sm"])
        text_center(draw, date, (828, y + 42, 1016, y + 100), PRIMARY_DEEP, F["label"])
        y += 158
    nav(draw, "Trail")
    return img


def badges_screen() -> Image.Image:
    img, draw = base()
    draw.text((64, 116), "Badges", fill=INK, font=F["h1"])
    draw.text((66, 188), "Small wins, collected as quiet stamps.", fill=MUTED, font=F["body"])
    paste_fit(img, sprite("badge.png"), (762, 82, 1002, 270))
    badges = [("badge.png", "First Step", True), ("category_cafe.png", "Cafe Quest", True), ("category_creative.png", "Maker", True), ("category_nature.png", "Fresh Air", False), ("category_reflection.png", "Reflector", False), ("category_explore.png", "Explorer", False)]
    for i, (art, label, earned) in enumerate(badges):
        left, top = 64 + (i % 2) * 490, 352 + (i // 2) * 418
        rounded(draw, (left, top, left + 448, top + 356), 42, SURFACE if earned else RAISED, BORDER, 2)
        paste_fit(img, sprite(art), (left + 86, top + 38, left + 362, top + 238), 1.0 if earned else 0.32)
        draw.text((left + 42, top + 262), label, fill=INK if earned else MUTED, font=F["h3"])
        draw.text((left + 42, top + 310), "Earned" if earned else "Locked", fill=PRIMARY if earned else QUIET, font=F["body_sm"])
    nav(draw, "Badges")
    return img


def profile_screen() -> Image.Image:
    img, draw = base()
    draw.text((64, 116), "Profile", fill=INK, font=F["h1"])
    draw.text((66, 188), "Private progress and account tools.", fill=MUTED, font=F["body"])
    rounded(draw, (54, 308, 1026, 574), 44, SURFACE, BORDER, 2)
    paste_fit(img, sprite("profile_cat_table.png"), (86, 332, 310, 548))
    draw.text((346, 360), "Questle Explorer", fill=INK, font=F["h2"])
    draw.text((348, 420), "Local-first, backed up when you sign in.", fill=MUTED, font=F["body_sm"])
    for i, (value, label) in enumerate([("7", "Streak"), ("18", "Done"), ("9", "Memories"), ("6", "Badges")]):
        x = 346 + i * 156
        draw.text((x, 484), value, fill=INK, font=F["h3"])
        draw.text((x, 526), label, fill=MUTED, font=F["tiny"])
    rounded(draw, (54, 654, 1026, 1078), 48, PRIMARY_DEEP)
    draw.line((120, 700, 872, 1016), fill="#8588F2", width=34)
    draw.text((116, 728), "Questle Pro", fill=SURFACE, font=F["h2"])
    draw_wrapped(draw, "Unlimited catalog picks, more custom Questles, photo memories, and richer saves.", (116, 792), width=610, fill="#F7F8FC", fnt=F["body"], max_lines=3)
    button(draw, (116, 954, 456, 1026), "Unlock Pro", fill=ACCENT)
    paste_fit(img, sprite("intro_memories.png"), (700, 718, 970, 1018))
    rounded(draw, (54, 1170, 1026, 1454), 42, SURFACE, BORDER, 2)
    draw.text((116, 1228), "Account Backup", fill=INK, font=F["h2"])
    draw_wrapped(draw, "Sign in with Google to prepare progress backup across devices. Photo memories stay on this device.", (116, 1290), width=800, fill=MUTED, fnt=F["body_sm"], max_lines=3)
    button(draw, (116, 1380, 462, 1434), "Google sign-in", fill=SURFACE, color=PRIMARY_DEEP, outline=PRIMARY_LINE)
    rounded(draw, (54, 1514, 1026, 1694), 40, SURFACE, BORDER, 2)
    draw.text((116, 1566), "Privacy", fill=INK, font=F["h3"])
    draw.text((116, 1616), "Export, restore, or delete your account data.", fill=MUTED, font=F["body_sm"])
    nav(draw, "Profile")
    return img


def intro_screen() -> Image.Image:
    img, draw = base()
    brand(img, draw)
    paste_fit(img, sprite("intro_discover.png"), (160, 188, 920, 770))
    draw_wrapped(draw, "Discover solo quests", (88, 854), width=820, fill=INK, fnt=F["h1"], max_lines=2)
    draw_wrapped(draw, "Browse small missions by mood, place, and energy. Start with one that feels easy today.", (88, 996), width=820, fill=MUTED, fnt=F["body"], max_lines=3)
    for i in range(4):
        x = 438 + i * 56
        draw.ellipse((x, 1208, x + 22, 1230), fill=PRIMARY_DEEP if i == 0 else BORDER)
    rounded(draw, (88, 1300, 992, 1514), 42, SURFACE, BORDER, 2)
    paste_fit(img, sprite("intro_choose.png"), (124, 1336, 334, 1480))
    draw.text((376, 1358), "Choose what fits your mood", fill=INK, font=F["h3"])
    draw_wrapped(draw, "Creative, cafe, nature, reflection, or explore.", (378, 1412), width=520, fill=MUTED, fnt=F["body_sm"], max_lines=2)
    button(draw, (88, 1650, 992, 1730), "Next")
    return img


def feature_graphic() -> Image.Image:
    img = rgb((1024, 500))
    draw = ImageDraw.Draw(img)
    paste_fit(img, sprite("logo.png"), (64, 56, 116, 108))
    draw.text((130, 60), "Questle", fill=PRIMARY, font=font(32))
    draw_wrapped(draw, "Tiny quests for ordinary days.", (64, 148), width=410, fill=INK, fnt=font(46), line_gap=2, max_lines=2)
    draw_wrapped(draw, "Browse a calm solo quest, complete it, and keep a private trail.", (66, 278), width=390, fill=MUTED, fnt=font(22), max_lines=3)
    button(draw, (66, 392, 288, 452), "Start a quest", fill=INK)
    paste_fit(img, sprite("home_greeting.png"), (520, 34, 984, 292))
    rounded(draw, (510, 282, 964, 456), 34, SURFACE, PRIMARY_LINE, 3)
    draw.text((540, 318), "Today's Questle", fill=PRIMARY_DEEP, font=font(24))
    draw_wrapped(draw, "Take yourself out for coffee", (540, 362), width=260, fill=INK, fnt=font(22), max_lines=2)
    paste_fit(img, sprite("category_cafe.png"), (796, 308, 934, 434))
    return img


def contact_sheet(assets: dict[str, Image.Image]) -> Image.Image:
    rows = []
    for name in ["feature-graphic-1024x500.png", "phone-01-home-catalog-1080x1920.png", "phone-02-quest-detail-1080x1920.png", "phone-03-quest-trail-1080x1920.png", "phone-04-badges-1080x1920.png", "phone-05-profile-pro-backup-1080x1920.png", "phone-06-feature-intro-1080x1920.png"]:
        image = assets[name]
        width = 512 if image.width > image.height else 260
        rows.append((name, image.resize((width, int(image.height * width / image.width)), Image.Resampling.LANCZOS)))
    sheet = rgb((620, 40 + sum(t.height + 78 for _, t in rows)))
    draw = ImageDraw.Draw(sheet)
    y = 28
    for name, thumb in rows:
        draw.text((32, y), name, fill=INK, font=font(18))
        y += 34
        sheet.paste(thumb, (32, y))
        y += thumb.height + 44
    return sheet


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
        image.save(OUT / name, optimize=True)
    sprite("app_icon.png").resize((512, 512), Image.Resampling.LANCZOS).save(OUT / "app-icon-512.png", optimize=True)
    contact_sheet(assets).save(OUT / "contact-sheet.png", optimize=True)
    (OUT / "listing-copy.md").write_text(
        "# Questle Google Play Listing Copy\n\n"
        "Short description: Tiny solo quests, private memories, and calm progress for ordinary days.\n\n"
        "Screenshot alt text:\n"
        "1. Home catalog showing the Questle greeting, Today's Questle, and browseable solo quest cards.\n"
        "2. Quest detail screen showing quest art, chips, how-to steps, and the Start Quest action.\n"
        "3. Quest Trail screen showing the month grid and memory ledger.\n"
        "4. Badges screen showing a collection-style grid of Questle stamps.\n"
        "5. Profile screen showing private stats, Pro benefits, and Account Backup.\n"
        "6. Feature intro screen showing the first solo-quest discovery panel.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    export()
