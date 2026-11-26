#!/usr/bin/env python3
"""Draw the world news of Thursday 26 November 2026 as one image.

Standard library only: no Pillow, no system fonts, no network, no
randomness and no clock, so the same bytes come out every time it runs
and it works on a bare grader box. The PNG is encoded by hand (zlib +
struct) and all text is drawn from an embedded 5x7 bitmap font.

Writes /output/entry.png when the grader's /output exists (or
MAKEFUN_OUTPUT_DIR is set), otherwise output/26-nov-2026-news.png
next to this file.
"""

import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (247, 244, 236)
INK = (24, 30, 46)
NAVY = (18, 38, 66)
CARD = (255, 255, 255)
MUTED = (92, 98, 110)
FOOTER = (120, 126, 138)

# ---------------------------------------------------------------- font
# Embedded 5x7 bitmap font. Each glyph is 7 rows of 5 bits, written as
# strings of "#" (on) and "." (off). Covers A-Z, a-z, 0-9 and punctuation.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10001", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    "g": ("00000", "00000", "01110", "10001", "10001", "01111", "01100"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "00010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    "q": ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11100", "01000", "01000", "01000", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01110", "00100", "01100"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "*": ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "[": ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    "]": ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "^": ("00100", "01010", "10001", "00000", "00000", "00000", "00000"),
    "~": ("00000", "00000", "01001", "10110", "00000", "00000", "00000"),
    "`": ("01000", "00100", "00000", "00000", "00000", "00000", "00000"),
    "{": ("00110", "01000", "01000", "11100", "01000", "01000", "00110"),
    "}": ("01100", "00010", "00010", "00111", "00010", "00010", "01100"),
    "\\": ("10000", "01000", "01000", "00100", "00010", "00010", "00001"),
}

# ---------------------------------------------------------------- canvas


class Canvas:
    """An RGB pixel buffer with tiny drawing primitives."""

    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, colour):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = colour

    def fill_rect(self, x0, y0, x1, y1, colour):
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(self.w - 1, x1)
        y1 = min(self.h - 1, y1)
        for y in range(y0, y1 + 1):
            i = (y * self.w + x0) * 3
            row = bytes(colour) * (x1 - x0 + 1)
            self.px[i:i + len(row)] = row

    def hline(self, x0, x1, y, colour, width=1):
        for t in range(width):
            self.fill_rect(x0, y + t, x1, y + t, colour)

    def vline(self, x, y0, y1, colour, width=1):
        for t in range(width):
            self.fill_rect(x + t, y0, x + t, y1, colour)

    def line(self, x0, y0, x1, y1, colour, width=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.fill_rect(x0 - width // 2, y0 - width // 2,
                           x0 + width // 2, y0 + width // 2, colour)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def fill_rounded_rect(self, x0, y0, x1, y1, r, colour):
        # Body: centre block plus side strips; corners cut by a circle test.
        self.fill_rect(x0 + r, y0, x1 - r, y1, colour)
        self.fill_rect(x0, y0 + r, x1, y1 - r, colour)
        for cx, cy in ((x0 + r, y0 + r), (x1 - r, y0 + r),
                       (x0 + r, y1 - r), (x1 - r, y1 - r)):
            for yy in range(cy - r, cy + r + 1):
                for xx in range(cx - r, cx + r + 1):
                    if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                        self.set(xx, yy, colour)

    def circle_outline(self, cx, cy, rx, ry, colour, width=1):
        import math
        steps = max(48, int(2 * 3.14159 * max(rx, ry)))
        prev = None
        for i in range(steps + 1):
            a = 2 * 3.14159 * i / steps
            x = cx + int(rx * math.cos(a))
            y = cy + int(ry * math.sin(a))
            if prev is not None:
                self.line(prev[0], prev[1], x, y, colour, width)
            prev = (x, y)

    def ellipse_fill(self, cx, cy, rx, ry, colour):
        import math
        for yy in range(cy - ry, cy + ry + 1):
            t = 1 - ((yy - cy) / ry) ** 2
            if t < 0:
                continue
            dx = int(rx * math.sqrt(t))
            self.fill_rect(cx - dx, yy, cx + dx, yy, colour)

    def polygon(self, points, colour):
        # Scanline fill.
        ys = [p[1] for p in points]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.fill_rect(int(xs[i]), y, int(xs[i + 1]), y, colour)

    def arc(self, cx, cy, rx, ry, a0, a1, colour, width=1):
        import math
        steps = 64
        prev = None
        for i in range(steps + 1):
            a = math.radians(a0 + (a1 - a0) * i / steps)
            x = cx + int(rx * math.cos(a))
            y = cy + int(ry * math.sin(a))
            if prev is not None:
                self.line(prev[0], prev[1], x, y, colour, width)
            prev = (x, y)

    # ---- text ----
    def glyph(self, x, y, ch, scale, colour, bold=False):
        rows = FONT.get(ch)
        if rows is None:
            return
        for r, row in enumerate(rows):
            for c, bit in enumerate(row):
                if bit == "1":
                    bx, by = x + c * scale, y + r * scale
                    self.fill_rect(bx, by, bx + scale - 1, by + scale - 1, colour)
                    if bold:
                        self.fill_rect(bx + 1, by, bx + scale, by + scale - 1, colour)

    def text(self, x, y, s, scale, colour, bold=False):
        for ch in s:
            self.glyph(x, y, ch, scale, colour, bold)
            x += 6 * scale
        return x

    def text_width(self, s, scale):
        return len(s) * 6 * scale - scale


def wrap(text, scale, max_width):
    """Greedy word wrap measured with the bitmap font."""
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if len(trial) * 6 * scale - scale <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


# ---------------------------------------------------------------- content

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


def icon(cv, kind, cx, cy, colour):
    """Small geometric pictogram centred at (cx, cy), ~64 px wide."""
    if kind == "bars":
        for i, h in enumerate((22, 38, 52)):
            x = cx - 30 + i * 22
            cv.fill_rect(x, cy + 26 - h, x + 14, cy + 26, colour)
        cv.hline(cx - 34, cx + 34, cy - 30, colour, 4)
    elif kind == "talks":
        cv.fill_rounded_rect(cx - 34, cy - 26, cx - 2, cy + 2, 8, colour)
        cv.fill_rounded_rect(cx + 2, cy - 2, cx + 34, cy + 26, 8, colour)
        cv.polygon([(cx - 28, cy + 2), (cx - 18, cy + 2), (cx - 30, cy + 16)], colour)
        cv.polygon([(cx + 28, cy - 2), (cx + 18, cy - 2), (cx + 30, cy - 16)], colour)
    elif kind == "flame":
        cv.polygon(
            [
                (cx, cy - 32), (cx + 16, cy - 6), (cx + 24, cy + 10),
                (cx + 10, cy + 26), (cx - 10, cy + 26), (cx - 24, cy + 10),
                (cx - 16, cy - 6),
            ],
            colour,
        )
        cv.ellipse_fill(cx, cy + 10, 7, 8, (255, 214, 90))
    elif kind == "atom":
        cv.ellipse_fill(cx, cy, 8, 8, colour)
        cv.circle_outline(cx, cy, 30, 14, colour, 4)
        cv.circle_outline(cx, cy, 14, 30, colour, 4)
    elif kind == "fall":
        cv.line(cx - 32, cy - 24, cx - 10, cy - 6, colour, 5)
        cv.line(cx - 10, cy - 6, cx + 8, cy - 14, colour, 5)
        cv.line(cx + 8, cy - 14, cx + 32, cy + 20, colour, 5)
        cv.polygon([(cx + 32, cy + 20), (cx + 32, cy + 6), (cx + 18, cy + 20)], colour)
        cv.hline(cx - 34, cx + 34, cy + 26, MUTED, 3)
    elif kind == "orbit":
        cv.arc(cx, cy, 34, 30, 200, 340, colour, 4)
        cv.fill_rect(cx - 8, cy - 6, cx + 8, cy + 6, colour)
        cv.fill_rect(cx - 26, cy - 3, cx - 10, cy + 3, colour)
        cv.fill_rect(cx + 10, cy - 3, cx + 26, cy + 3, colour)
        cv.line(cx + 8, cy - 6, cx + 16, cy - 16, colour, 3)
        cv.ellipse_fill(cx + 17, cy - 15, 3, 3, colour)


def draw_card(cv, x, y, w, h, story):
    tag, accent, headline, body, kind = story
    cv.fill_rounded_rect(x, y, x + w, y + h, 14, CARD)
    cv.fill_rect(x, y, x + w, y + 10, accent)
    cv.fill_rect(x, y + 5, x + w, y + 10, accent)
    pad = 22
    tx = x + pad
    ty = y + 22
    cv.text(tx, ty, tag, 3, accent, bold=True)
    ty += 21 + 10
    for line in wrap(headline, 3, w - 2 * pad):
        cv.text(tx, ty, line, 3, INK, bold=True)
        ty += 26
    ty += 6
    for line in wrap(body, 2, w - 2 * pad - 78):
        cv.text(tx, ty, line, 2, MUTED)
        ty += 20
    icon(cv, kind, x + w - 52, y + h - 48, accent)


def build():
    cv = Canvas(W, H, PAPER)

    # Masthead.
    cv.fill_rect(0, 0, W - 1, 157, NAVY)
    cv.text(32, 26, "WORLD NEWS", 8, (255, 255, 255), bold=True)
    cv.text(32, 100, "Thursday 26 November 2026", 4, (176, 196, 224))
    gx, gy = 936, 79
    cv.circle_outline(gx, gy, 42, 42, (255, 255, 255), 4)
    cv.circle_outline(gx, gy, 18, 42, (255, 255, 255), 3)
    cv.hline(gx - 42, gx + 42, gy, (255, 255, 255), 3)

    # 2 x 3 cards.
    margin, gap = 16, 16
    cw = (W - 2 * margin - gap) // 2
    ch = 252
    top = 172
    for i, story in enumerate(STORIES):
        row, col = divmod(i, 2)
        x = margin + col * (cw + gap)
        y = top + row * (ch + gap)
        draw_card(cv, x, y, cw, ch, story)

    # Footer.
    cv.text(
        32, H - 28,
        "Sources: Reuters, AP, Al Jazeera, The Hindu, Japan Times  |  "
        "One day, six stories",
        2, FOOTER,
    )
    return cv


# ---------------------------------------------------------------- PNG

def png_bytes(cv):
    def chunk(typ, data):
        return (
            struct.pack(">I", len(data))
            + typ
            + data
            + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)  # filter: none
        raw += cv.px[y * stride:(y + 1) * stride]
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        name = "entry.png"
    elif os.path.isdir("/output"):
        out_dir, name = "/output", "entry.png"
    else:
        out_dir, name = "output", "26-nov-2026-news.png"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    with open(path, "wb") as f:
        f.write(png_bytes(build()))
    print(path)


if __name__ == "__main__":
    main()
