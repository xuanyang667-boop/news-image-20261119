#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page (1024x1024 PNG).

Deterministic: no network, no randomness, no timestamps. The same script
always writes the same bytes (PNG encoder output is deterministic for the
same input pixels with fixed settings).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (25, 25, 25)
RED = (166, 30, 30)
NAVY = (30, 58, 95)
GOLD = (194, 154, 43)
TEAL = (31, 111, 107)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF_B = os.path.join(FONT_DIR, "NotoSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
SANS_SB = os.path.join(FONT_DIR, "NotoSans-SemiBold.ttf")
SANS = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def letterspaced(draw, cx, y, text, fnt, fill, spacing=6):
    """Draw text centred on cx with extra letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + spacing


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_scales(draw, cx, top, scale, gold=GOLD):
    """Scales of justice, centred on cx, top of the pillar at top."""
    s = scale
    draw.line([(cx, top), (cx, top + 150 * s)], fill=gold, width=max(3, int(7 * s)))
    draw.line([(cx - 42 * s, top + 158 * s), (cx + 42 * s, top + 158 * s)],
              fill=gold, width=max(3, int(7 * s)))
    draw.line([(cx - 78 * s, top + 22 * s), (cx + 78 * s, top + 22 * s)],
              fill=gold, width=max(3, int(6 * s)))
    draw.ellipse([cx - 7 * s, top - 12 * s, cx + 7 * s, top + 2 * s], fill=gold)
    for side in (-1, 1):
        px = cx + side * 78 * s
        draw.line([(px, top + 22 * s), (px - 30 * s, top + 78 * s)], fill=gold, width=max(2, int(4 * s)))
        draw.line([(px, top + 22 * s), (px + 30 * s, top + 78 * s)], fill=gold, width=max(2, int(4 * s)))
        draw.pieslice([px - 32 * s, top + 66 * s, px + 32 * s, top + 106 * s],
                      start=0, end=180, fill=gold)


def draw_flag(draw, x, y, w, h, kind):
    """Tiny simplified flag in a rounded box."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, outline=INK, width=2)
    if kind == "usa":
        for i in range(7):
            col = (178, 34, 34) if i % 2 == 0 else WHITE
            draw.rectangle([x + 2, y + 2 + i * (h - 4) / 7, x + w - 2, y + 2 + (i + 1) * (h - 4) / 7], fill=col)
        draw.rectangle([x + 2, y + 2, x + w * 0.42, y + h * 0.55], fill=NAVY)
        for sx in (0.12, 0.22, 0.32):
            for sy in (0.15, 0.32):
                draw.ellipse([x + w * sx - 2, y + h * sy - 2, x + w * sx + 2, y + h * sy + 2], fill=WHITE)
    elif kind == "chn":
        draw.rectangle([x + 2, y + 2, x + w - 2, y + h - 2], fill=(222, 41, 16))
        cx, cy, r = x + w * 0.24, y + h * 0.30, 7
        draw.regular_polygon((cx, cy, r), n_sides=5, fill=GOLD)
        draw.regular_polygon((x + w * 0.45, y + h * 0.55, 3), n_sides=5, fill=GOLD)
    elif kind == "rus":
        stripe = (h - 4) / 3
        for i, col in enumerate([WHITE, (0, 57, 166), (213, 0, 50)]):
            draw.rectangle([x + 2, y + 2 + i * stripe, x + w - 2, y + 2 + (i + 1) * stripe], fill=col)


def draw_bars(draw, x, y, w, h, values, colors):
    n = len(values)
    bw = w / n * 0.55
    gap = w / n * 0.45
    mx = max(values)
    for i, v in enumerate(values):
        bh = h * v / mx
        bx = x + i * (bw + gap) + gap / 2
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=colors[i % len(colors)])
    draw.line([(x, y + h), (x + w, y + h)], fill=INK, width=3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead (0..212) ----------
    d.text((W // 2, 14), "THE WORLD", font=font(SERIF_B, 96), fill=INK, anchor="ma")
    letterspaced(d, W // 2, 118, "IN ONE IMAGE", font(SANS_B, 26), INK, spacing=10)
    rule(d, 60, 964, 158, fill=INK, width=3)
    d.text((W // 2, 168), "THURSDAY  ·  19 NOVEMBER 2026", font=font(SANS_B, 30),
           fill=RED, anchor="ma")
    rule(d, 60, 964, 212, fill=RED, width=2)

    # ---------- lead story (232..508) ----------
    lx, lw = 40, 556
    d.text((lx, 236), "THE HAGUE  —  TOP STORY", font=font(SANS_B, 23), fill=RED)
    y = draw_wrapped(d, lx, 272, "World court: Myanmar guilty of Rohingya genocide",
                     font(SERIF_B, 42), lw, leading=48)
    draw_wrapped(d, lx, 430,
                 "The International Court of Justice ruled on Thursday that Myanmar's "
                 "military acted with genocidal intent in 2017 — and ordered restitution.",
                 font(SANS, 22), lw, leading=28)

    # lead visual: scales of justice
    px0, py0, px1, py1 = 620, 232, 984, 500
    d.rounded_rectangle([px0, py0, px1, py1], radius=10, fill=NAVY)
    draw_scales(d, (px0 + px1) // 2, py0 + 44, 0.8)
    d.text(((px0 + px1) // 2, py1 - 40), "The Peace Palace, The Hague",
           font=font(SANS_SB, 20), fill=WHITE, anchor="ma")

    rule(d, 40, 984, 522, fill=INK, width=2)

    # ---------- middle row (538..806) ----------
    # Summit (left)
    mx, mw = 40, 452
    d.text((mx, 538), "SHENZHEN  —  SUMMIT", font=font(SANS_B, 22), fill=RED)
    draw_wrapped(d, mx, 566, "Trump, Xi and Putin sign a “Declaration toward Peace”",
                 font(SERIF_B, 30), mw, leading=36)
    draw_wrapped(d, mx, 644,
                 "First three-way summit of the US, Chinese and Russian leaders "
                 "pledges nuclear-risk talks.",
                 font(SANS, 20), mw, leading=26)
    fy = 730
    for i, (kind, label) in enumerate([("usa", "USA"), ("chn", "CHINA"), ("rus", "RUSSIA")]):
        fx = mx + i * 150
        draw_flag(d, fx, fy, 118, 56, kind)
        d.text((fx + 59, fy + 62), label, font=font(SANS_B, 16), fill=INK, anchor="ma")

    # IPO (right)
    rx, rw = 532, 452
    d.text((rx, 538), "WALL STREET", font=font(SANS_B, 22), fill=RED)
    draw_wrapped(d, rx, 566, "Anthropic's $83 IPO values the AI firm at $1.5 trillion",
                 font(SERIF_B, 30), rw, leading=36)
    draw_wrapped(d, rx, 644,
                 "Shares priced Wednesday in a record offering; Nasdaq trading "
                 "began Thursday.",
                 font(SANS, 20), rw, leading=26)
    draw_bars(d, rx, 730, 300, 56, [0.35, 0.6, 1.0], [TEAL, TEAL, GOLD])
    d.text((rx + 316, 748), "$83", font=font(SANS_B, 28), fill=INK)

    rule(d, 40, 984, 820, fill=INK, width=2)

    # ---------- briefs (836..960) ----------
    d.text((40, 836), "ALSO ON 19 NOVEMBER", font=font(SANS_B, 24), fill=INK)
    briefs = [
        ("BANGLADESH", "Unrest hits 28 districts; Yunus's ancestral home torched."),
        ("COP31 · ANTALYA", "Ministers meet to unblock climate talks and agree a text."),
        ("STRAIT OF HORMUZ", "Tanker attacks mount as US–Iran strikes escalate."),
        ("GREENLAND", "Denmark ratifies the US security pact unanimously."),
    ]
    for i, (kick, text) in enumerate(briefs):
        x = 40 + i * 242
        d.text((x, 872), kick, font=font(SANS_B, 18), fill=RED)
        draw_wrapped(d, x, 898, text, font(SANS, 19), 226, leading=23)

    # ---------- footer ----------
    rule(d, 40, 984, 972, fill=INK, width=2)
    d.text((W // 2, 982), "19 NOVEMBER 2026  ·  THE WORLD'S NEWS IN ONE IMAGE",
           font=font(SANS_B, 19), fill=GREY, anchor="ma")
    return img


if __name__ == "__main__":
    out = os.environ.get("OUT", "assets/entry.png")
    img = build()
    img.save(out, "PNG", optimize=True)
    print(out, img.size, os.path.getsize(out), "bytes")
