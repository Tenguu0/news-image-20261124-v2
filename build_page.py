#!/usr/bin/env python3
"""Build the 24 Nov 2026 front page ("The World in One Page").

Written fresh in this session. Composites the AI-generated text-free
lead illustration (lead.webp) with PIL/DejaVu typesetting; all other
pictures are flat pictograms drawn with PIL primitives, scaled to the
box height they are given. Deterministic: no network, no randomness,
no clock. Writes entry.png (1024x1024).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28  # margin
PAPER = (251, 247, 238)
INK = (22, 21, 19)
NAVY = (16, 36, 62)
RED = (180, 35, 24)
GOLD = (201, 162, 39)
GREY = (120, 118, 112)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    leading = leading or int(fnt.size * 1.25)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, lines, fnt, fill=INK, leading=None):
    leading = leading or int(fnt.size * 1.05)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------- pictograms (all coordinates relative to box height h) ----------
def pic_ukraine(d, x, y, w, h):
    top = y + int(0.18 * h)
    # Dark broken apartment block, left.
    d.rectangle([x, top, x + 96, y + h], fill=(52, 50, 48))
    for k, wy in enumerate((0.30, 0.50, 0.70)):
        yy = y + int(wy * h)
        for wx in (x + 12, x + 40, x + 68):
            d.rectangle([wx, yy, wx + 16, yy + 11], fill=GOLD)
    d.polygon([(x + 96, top), (x + 96, y + int(0.42 * h)),
               (x + 128, y + int(0.58 * h)), (x + 128, y + h)],
              fill=(52, 50, 48))
    # Damaged grey block, right.
    gx = x + 148
    d.rectangle([gx, y + int(0.34 * h), x + w - 6, y + h],
                fill=(150, 148, 142))
    d.rectangle([gx + 12, y + int(0.46 * h), gx + 28, y + int(0.60 * h)],
                fill=INK)
    d.rectangle([gx + 46, y + int(0.46 * h), gx + 62, y + int(0.60 * h)],
                fill=INK)
    d.polygon([(gx, y + int(0.34 * h)), (gx + 18, y + int(0.52 * h)),
               (gx + 36, y + int(0.34 * h))], fill=(150, 148, 142))
    # Rubble + rescue light.
    d.polygon([(x + 118, y + h - 22), (x + 158, y + h - 22),
               (x + 178, y + h), (x + 98, y + h)], fill=(90, 88, 84))
    d.ellipse([x + 126, y + h - 38, x + 136, y + h - 28], fill=RED)
    d.line([x, y + h, x + w, y + h], fill=INK, width=2)


def pic_chairs(d, x, y, w, h):
    # Three empty summit chairs above a table line; red NO DEAL banner.
    seat_y = int(0.10 * h)
    for cx in (x + 28, x + 128, x + 228):
        d.rectangle([cx, y + seat_y, cx + 62, y + seat_y + 34], fill=NAVY)
        d.rectangle([cx + 6, y + seat_y + 34, cx + 12, y + int(0.62 * h)],
                    fill=NAVY)
        d.rectangle([cx + 50, y + seat_y + 34, cx + 56, y + int(0.62 * h)],
                    fill=NAVY)
    d.rectangle([x, y + int(0.62 * h), x + w, y + int(0.66 * h)],
                fill=(90, 88, 84))
    by = y + int(0.70 * h)
    d.rectangle([x, by, x + w, y + h], fill=RED)
    f = SANS_B(max(14, int(0.20 * h)))
    t = "NO DEAL"
    d.text((x + (w - d.textlength(t, font=f)) / 2,
            by + (h - int(0.70 * h) - f.size) // 2), t,
           font=f, fill=(255, 255, 255))
    # Fallen gavel on the table.
    d.rectangle([x + 236, y + int(0.58 * h), x + 290, y + int(0.62 * h)],
                fill=GOLD)


def pic_scales(d, x, y, w, h):
    cx = x + w // 2
    d.rectangle([cx - 3, y + int(0.06 * h), cx + 3, y + int(0.82 * h)],
                fill=GOLD)
    d.ellipse([cx - 7, y, cx + 7, y + 14], fill=GOLD)
    beam = y + int(0.24 * h)
    d.line([cx - 58, beam, cx + 58, beam], fill=GOLD, width=4)
    for sx in (cx - 58, cx + 58):
        pan = y + int(0.52 * h)
        d.line([sx, beam, sx - 24, pan], fill=GOLD, width=3)
        d.line([sx, beam, sx + 24, pan], fill=GOLD, width=3)
        d.polygon([(sx - 28, pan), (sx + 28, pan),
                   (sx, y + int(0.80 * h))], fill=GOLD)
    d.rectangle([cx - 32, y + int(0.86 * h), cx + 32, y + int(0.92 * h)],
                fill=GOLD)


def pic_flags(d, x, y, w, h):
    # China, USA, Russia — small flags on poles, no likenesses.
    fw, fh = 72, int(0.52 * h)
    gap = (w - 3 * fw) // 2
    # China
    fx = x
    d.rectangle([fx, y, fx + fw, y + fh], fill=(222, 41, 16))
    d.ellipse([fx + 10, y + 7, fx + 22, y + 19], fill=GOLD)
    for sx, sy in ((fx + 34, y + 7), (fx + 44, y + 15),
                   (fx + 40, y + 26), (fx + 28, y + 28)):
        d.ellipse([sx, sy, sx + 6, sy + 6], fill=GOLD)
    # USA
    fx = x + fw + gap
    for i in range(7):
        d.rectangle([fx, y + i * fh // 7, fx + fw, y + (i + 1) * fh // 7],
                    fill=RED if i % 2 == 0 else (255, 255, 255))
    d.rectangle([fx, y, fx + 30, y + fh * 3 // 7], fill=NAVY)
    # Russia
    fx = x + 2 * (fw + gap)
    d.rectangle([fx, y, fx + fw, y + fh // 3], fill=(255, 255, 255))
    d.rectangle([fx, y + fh // 3, fx + fw, y + 2 * fh // 3],
                fill=(0, 57, 166))
    d.rectangle([fx, y + 2 * fh // 3, fx + fw, y + fh], fill=(213, 0, 50))
    for fx in (x, x + fw + gap, x + 2 * (fw + gap)):
        d.line([fx + fw // 2, y + fh, fx + fw // 2, y + int(0.92 * h)],
               fill=INK, width=3)
        d.ellipse([fx + fw // 2 - 4, y + int(0.90 * h),
                   fx + fw // 2 + 4, y + int(0.98 * h)], fill=GOLD)


def pic_trophy(d, x, y, w, h):
    cx = x + w // 2
    cup_t, cup_b = y + int(0.04 * h), y + int(0.56 * h)
    d.polygon([(cx - 42, cup_t), (cx + 42, cup_t), (cx + 28, cup_b),
               (cx - 28, cup_b)], fill=GOLD)
    d.arc([cx - 60, cup_t, cx - 24, cup_t + 34], 90, 270, fill=GOLD,
          width=5)
    d.arc([cx + 24, cup_t, cx + 60, cup_t + 34], -90, 90, fill=GOLD,
          width=5)
    d.rectangle([cx - 5, cup_b, cx + 5, y + int(0.70 * h)], fill=GOLD)
    d.rectangle([cx - 26, y + int(0.70 * h), cx + 26, y + int(0.78 * h)],
                fill=GOLD)
    d.ellipse([cx + 32, y + int(0.62 * h), cx + 62, y + int(0.92 * h)],
              fill=(139, 195, 74))
    d.arc([cx + 36, y + int(0.66 * h), cx + 58, y + int(0.88 * h)],
          200, 340, fill=(255, 255, 255), width=3)


# ---------- page ----------
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([M - 4, M - 4, W - M + 4, H - M + 4], outline=INK, width=3)

    # Masthead (28..128)
    d.rectangle([M, M, W - M, 128], fill=NAVY)
    f_name = SERIF_B(60)
    name = "THE GLOBAL HERALD"
    d.text(((W - d.textlength(name, font=f_name)) / 2, M + 8), name,
           font=f_name, fill=(255, 255, 255))
    d.line([M + 30, 96, W - M - 30, 96], fill=GOLD, width=3)
    f_date = SANS_B(22)
    date = "TUESDAY, 24 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 102), date,
           font=f_date, fill=(255, 255, 255))

    # Lead: picture left (140..380), text right
    lead = Image.open("lead.webp").convert("RGB")
    lw, lh = 372, 240
    lead = lead.resize((lw, int(lead.height * lw / lead.width)))
    top = max(0, (lead.height - lh) // 2)
    lead = lead.crop((0, top, lw, top + lh))
    img.paste(lead, (M, 140))
    d.rectangle([M, 140, M + lw, 140 + lh], outline=INK, width=2)

    tx = M + lw + 18
    tw = W - M - tx
    y = 140
    d.text((tx, y), "GULF WAR WIDENS  \u2022  BAHRAIN, SATURDAY NIGHT",
           font=SANS_B(19), fill=RED)
    y = 168
    y = headline(d, tx, y, ["IRAN HITS", "US BASES"], SERIF_B(58))
    y += 4
    y = para(d, tx, y,
             "TEHRAN CLAIMS TWO PATRIOT RADARS HIT; BAHRAIN SAYS A "
             "CIVILIAN SITE BURNED, 2 HURT.",
             SANS(21), tw)
    y += 2
    y = para(d, tx, y,
             "TRUMP WARNS OF \u201cVERY TRAUMATIC\u201d OUTCOME",
             SANS_B(20), tw, fill=RED)
    y = para(d, tx, y, "25 SHIPS HIT IN HORMUZ IN A WEEK.",
             SANS_B(20), tw)
    d.line([M, 406, W - M, 406], fill=INK, width=2)

    # Row 2 (418..644), two columns
    mid = W // 2
    colw = mid - M - 16
    pic_ukraine(d, M, 418, colw, 72)
    d.text((M, 496), "UKRAINE", font=SANS_B(20), fill=RED)
    y = headline(d, M, 520, ["15 DEAD IN KYIV", "REGION"], SERIF_B(38))
    para(d, M, 604,
         "FIFTH WAR WINTER BEGINS; THE GRID IS UNDER FIRE AND PATRIOT "
         "STOCKS ARE EXHAUSTED.",
         SANS(18), colw)
    d.line([mid, 418, mid, 644], fill=GREY, width=1)
    rx = mid + 16
    pic_chairs(d, rx, 418, colw, 72)
    d.text((rx, 496), "CLIMATE FALLOUT", font=SANS_B(20), fill=RED)
    y = headline(d, rx, 520, ["COP31 IN RUINS"], SERIF_B(38))
    para(d, rx, 604,
         "GUTERRES \u201cDEEPLY DISAPPOINTED\u201d; \u201cWORST EVER COP\u201d "
         "AS 194 NATIONS SPLIT OVER FOSSIL FUELS.",
         SANS(18), colw)
    d.line([M, 656, W - M, 656], fill=INK, width=2)

    # Row 3 (668..856), three columns
    cw = (W - 2 * M - 32) // 3
    cols = [
        ("WORLD COURT", ["MYANMAR GUILTY", "OF GENOCIDE"], pic_scales,
         "FIRST STATE EVER CONVICTED; 9\u20136, 10,000 KILLED."),
        ("SHENZHEN", ["THREE POWERS", "TALK, NO DEAL"], pic_flags,
         "XI, TRUMP, PUTIN MEET; NO UKRAINE BREAKTHROUGH."),
        ("SPORT  \u2022  TENNIS", ["ALCARAZ WINS", "ATP FINALS"],
         pic_trophy, "6-2, 7-6 OVER ZVEREV; FIRST TITLE; $5.17M."),
    ]
    for i, (kick, head, pic, deck) in enumerate(cols):
        cx = M + i * (cw + 16)
        if i:
            d.line([cx - 8, 668, cx - 8, 856], fill=GREY, width=1)
        d.text((cx, 668), kick, font=SANS_B(18), fill=RED)
        headline(d, cx, 692, head, SERIF_B(29))
        pic(d, cx, 756, cw, 64)
        para(d, cx, 824, deck, SANS(17), cw)
    d.line([M, 872, W - M, 872], fill=INK, width=2)

    # MEANWHILE strip (884..992)
    y = 884
    d.text((M, y), "MEANWHILE", font=SANS_B(18), fill=RED)
    rest = "  \u2014  SOURCES: AL JAZEERA, AFP, REUTERS, AP, CNN, UN NEWS, HRW"
    d.text((M + d.textlength("MEANWHILE", font=SANS_B(18)), y), rest,
           font=SANS(16), fill=INK)
    items = [
        ("USA: ", "AMTRAK DERAILS IN LOUISIANA \u2014 95 ABOARD, 5 HURT"),
        ("TECH: ", "WAYMO PULLS ROBOTAXIS OFF ALL US FREEWAYS"),
        ("SUDAN: ", "DRONE STRIKES NEAR KHARTOUM KILL 4, HIT UN BUILDING"),
        ("ASIA: ", "THAI\u2013CAMBODIA BORDER TRUCE HOLDS"),
    ]
    y = 910
    for label, text in items:
        d.text((M, y), label, font=SANS_B(16), fill=RED)
        d.text((M + d.textlength(label, font=SANS_B(16)), y), text,
               font=SANS(16), fill=INK)
        y += 20

    img.save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    build()
