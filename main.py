#!/usr/bin/env python3
"""Draw the world news of Thursday 26 November 2026 as one image.

Reads nothing, uses no network, no randomness and no clock: the same
bytes come out every time it runs. Writes /output/entry.png when the
grader's /output exists (or MAKEFUN_OUTPUT_DIR is set), otherwise
output/26-nov-2026-news.png next to this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 244, 236)
INK = (24, 30, 46)
NAVY = (18, 38, 66)
CARD = (255, 255, 255)
MUTED = (92, 98, 110)
FOOTER = (120, 126, 138)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
TITLE_FONT = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 64)
DATE_FONT = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), 30)
TAG_FONT = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 21)
HEAD_FONT = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 28)
BODY_FONT = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), 23)
FOOT_FONT = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), 19)

# (tag, accent colour, headline, body, icon)
STORIES = [
    (
        "TRADE",
        (196, 84, 32),
        "US unveils new tariffs on 14 partners",
        "Washington proposes tariffs on China, the EU and others; "
        "25% on India, citing excess capacity.",
        "bars",
    ),
    (
        "UKRAINE",
        (42, 96, 150),
        "Peace talks in Abu Dhabi end with no deal",
        "Russia holds its territorial claims; Kyiv says it hit a "
        "Russian air base, damaging five planes.",
        "talks",
    ),
    (
        "EGYPT",
        (178, 44, 44),
        "Fuel tanker fire kills at least 31 near Cairo",
        "A tanker overturned on Cairo's Ring Road and burst into "
        "flames, engulfing cars; 21 hurt.",
        "flame",
    ),
    (
        "NORTH KOREA",
        (110, 66, 140),
        "Kim orders wider tactical nuclear deployment",
        "Pyongyang's leader wants tactical nuclear arms spread "
        "more widely across its units.",
        "atom",
    ),
    (
        "MARKETS",
        (30, 128, 96),
        "AI sell-off drags US stocks into correction",
        "The S&P 500 and the Dow slide as doubts over AI spending "
        "hit technology shares.",
        "fall",
    ),
    (
        "SPACE",
        (30, 84, 140),
        "SpaceX cleared to put data centres in orbit",
        "The FCC approves up to one million orbital compute "
        "modules for its Starmind network.",
        "orbit",
    ),
]


def wrap(draw, text, font, max_width):
    """Greedy word wrap measured with the real font."""
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def icon(draw, kind, cx, cy, colour):
    """Small geometric pictogram centred at (cx, cy), ~64 px wide."""
    if kind == "bars":
        heights = [22, 38, 52]
        for i, h in enumerate(heights):
            x = cx - 30 + i * 22
            draw.rectangle([x, cy + 26 - h, x + 14, cy + 26], fill=colour)
        draw.line([cx - 34, cy - 30, cx + 34, cy - 30], fill=colour, width=4)
    elif kind == "talks":
        draw.rounded_rectangle(
            [cx - 34, cy - 24, cx - 2, cy + 4], radius=8, outline=colour, width=4
        )
        draw.rounded_rectangle(
            [cx + 2, cy - 4, cx + 34, cy + 24], radius=8, outline=colour, width=4
        )
        draw.polygon(
            [(cx - 28, cy + 2), (cx - 18, cy + 2), (cx - 30, cy + 16)], fill=colour
        )
        draw.polygon(
            [(cx + 28, cy - 2), (cx + 18, cy - 2), (cx + 30, cy - 16)], fill=colour
        )
    elif kind == "flame":
        draw.polygon(
            [
                (cx, cy - 32),
                (cx + 16, cy - 6),
                (cx + 24, cy + 10),
                (cx + 10, cy + 26),
                (cx - 10, cy + 26),
                (cx - 24, cy + 10),
                (cx - 16, cy - 6),
            ],
            fill=colour,
        )
        draw.ellipse([cx - 7, cy + 2, cx + 7, cy + 18], fill=(255, 214, 90))
    elif kind == "atom":
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=colour)
        draw.arc([cx - 30, cy - 14, cx + 30, cy + 14], 0, 360, fill=colour, width=4)
        draw.arc([cx - 14, cy - 30, cx + 14, cy + 30], 0, 360, fill=colour, width=4)
    elif kind == "fall":
        draw.line(
            [(cx - 32, cy - 24), (cx - 10, cy - 6), (cx + 8, cy - 14), (cx + 32, cy + 20)],
            fill=colour,
            width=5,
        )
        draw.polygon(
            [(cx + 32, cy + 20), (cx + 32, cy + 6), (cx + 18, cy + 20)], fill=colour
        )
        draw.line([cx - 34, cy + 26, cx + 34, cy + 26], fill=MUTED, width=3)
    elif kind == "orbit":
        draw.arc([cx - 34, cy - 30, cx + 34, cy + 30], 200, 340, fill=colour, width=4)
        draw.rectangle([cx - 8, cy - 6, cx + 8, cy + 6], fill=colour)
        draw.rectangle([cx - 26, cy - 3, cx - 10, cy + 3], fill=colour)
        draw.rectangle([cx + 10, cy - 3, cx + 26, cy + 3], fill=colour)
        draw.line([cx + 8, cy - 6, cx + 16, cy - 16], fill=colour, width=3)
        draw.ellipse([cx + 14, cy - 18, cx + 20, cy - 12], fill=colour)


def draw_card(draw, x, y, w, h, story):
    tag, accent, headline, body, kind = story
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=CARD)
    draw.rounded_rectangle([x, y, x + w, y + 10], radius=5, fill=accent)
    draw.rectangle([x, y + 5, x + w, y + 10], fill=accent)
    pad = 22
    tx, ty = x + pad, y + 24
    draw.text((tx, ty), tag, font=TAG_FONT, fill=accent)
    ty += 34
    for line in wrap(draw, headline, HEAD_FONT, w - 2 * pad):
        draw.text((tx, ty), line, font=HEAD_FONT, fill=INK)
        ty += 34
    ty += 4
    for line in wrap(draw, body, BODY_FONT, w - 2 * pad - 78):
        draw.text((tx, ty), line, font=BODY_FONT, fill=MUTED)
        ty += 29
    icon(draw, kind, x + w - 52, y + h - 48, accent)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead.
    draw.rectangle([0, 0, W, 158], fill=NAVY)
    draw.text((32, 26), "WORLD NEWS", font=TITLE_FONT, fill=(255, 255, 255))
    draw.text(
        (32, 104), "Thursday 26 November 2026", font=DATE_FONT, fill=(176, 196, 224)
    )
    # Globe mark in the masthead.
    gx, gy = 936, 79
    draw.ellipse([gx - 42, gy - 42, gx + 42, gy + 42], outline=(255, 255, 255), width=4)
    draw.ellipse([gx - 18, gy - 42, gx + 18, gy + 42], outline=(255, 255, 255), width=3)
    draw.line([gx - 42, gy, gx + 42, gy], fill=(255, 255, 255), width=3)

    # 2 x 3 cards.
    margin, gap = 16, 16
    cw = (W - 2 * margin - gap) // 2
    ch = 252
    top = 172
    for i, story in enumerate(STORIES):
        row, col = divmod(i, 2)
        x = margin + col * (cw + gap)
        y = top + row * (ch + gap)
        draw_card(draw, x, y, cw, ch, story)

    # Footer.
    draw.text(
        (32, H - 30),
        "Sources: Reuters, AP, Al Jazeera, The Hindu, Japan Times  |  One day, six stories",
        font=FOOT_FONT,
        fill=FOOTER,
    )
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        name = "entry.png"
    elif os.path.isdir("/output"):
        out_dir, name = "/output", "entry.png"
    else:
        out_dir, name = "output", "26-nov-2026-news.png"
    os.makedirs(out_dir, exist_ok=True)
    build().save(os.path.join(out_dir, name), format="PNG")
    print(os.path.join(out_dir, name))


if __name__ == "__main__":
    main()
