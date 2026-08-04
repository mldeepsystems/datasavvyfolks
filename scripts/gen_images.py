#!/usr/bin/env python3
"""Generate OG share image, favicon PNG, and apple-touch-icon for Data Savvy Folks."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "/Volumes/AnmolxHDD/Anmol/Macbook Pro Backup/Documents/GitHub/datasavvyfolks"

# ---- Brand colors ----
BERRY  = (255, 46, 147)
VIOLET = (139, 92, 255)
BLUE   = (46, 123, 255)
WHITE  = (255, 255, 255)

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def diagonal_gradient(w, h, stops):
    """stops: list of (pos0..1, color). Diagonal (top-left -> bottom-right)."""
    base = Image.new("RGB", (w, h))
    px = base.load()
    maxd = w + h
    for y in range(h):
        for x in range(w):
            t = (x + y) / maxd
            # find segment
            for i in range(len(stops) - 1):
                p0, c0 = stops[i]
                p1, c1 = stops[i + 1]
                if p0 <= t <= p1:
                    lt = (t - p0) / (p1 - p0) if p1 > p0 else 0
                    px[x, y] = lerp(c0, c1, lt)
                    break
            else:
                px[x, y] = stops[-1][1]
    return base

def load_font(size, weight="bold"):
    candidates = {
        "bold": [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/Library/Fonts/Arial Bold.ttf",
        ],
        "regular": [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ],
    }
    for path in candidates[weight]:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius=radius, fill=255)
    return m

def text_w(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0]

# ============================================================
# 1. OG IMAGE (1200 x 630)
# ============================================================
W, H = 1200, 630
og = diagonal_gradient(W, H, [(0.0, BERRY), (0.5, VIOLET), (1.0, BLUE)])
draw = ImageDraw.Draw(og, "RGBA")

# translucent decorative blobs
blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(blob)
bd.ellipse([880, -140, 1340, 320], fill=(255, 255, 255, 26))
bd.ellipse([-160, 360, 300, 820], fill=(255, 255, 255, 22))
og.paste(Image.alpha_composite(og.convert("RGBA"), blob).convert("RGB"), (0, 0))
draw = ImageDraw.Draw(og, "RGBA")

PADX = 80

# --- wordmark chip (bar chart icon + name) ---
chip_y = 70
# small rounded icon
icon = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
idr = ImageDraw.Draw(icon)
idr.rounded_rectangle([0, 0, 63, 63], radius=18, fill=(255, 255, 255, 235))
for (bx, by, bh) in [(16, 34, 16), (28, 24, 26), (40, 16, 34)]:
    idr.rounded_rectangle([bx, by, bx+8, by+bh], radius=3, fill=VIOLET)
og.paste(icon, (PADX, chip_y), icon)
f_word = load_font(34, "bold")
draw.text((PADX + 80, chip_y + 14), "Data Savvy Folks", font=f_word, fill=WHITE)

# --- headline ---
f_head = load_font(88, "bold")
draw.text((PADX, 210), "Where data people", font=f_head, fill=WHITE)
draw.text((PADX, 310), "grow together", font=f_head, fill=(230, 240, 255))

# --- subline ---
f_sub = load_font(30, "regular")
draw.text((PADX, 430),
          "Analysts · Engineers · Data Scientists · ML/AI · GenAI",
          font=f_sub, fill=(240, 235, 255))

# --- stat pill ---
pill_text = "260+ members  ·  Free mentorship & events  ·  Join us"
f_pill = load_font(26, "bold")
pw = text_w(draw, pill_text, f_pill)
pill_x, pill_y = PADX, 500
draw.rounded_rectangle([pill_x, pill_y, pill_x + pw + 56, pill_y + 56],
                       radius=28, fill=(255, 255, 255, 235))
draw.text((pill_x + 28, pill_y + 12), pill_text, font=f_pill, fill=VIOLET)

# --- sponsor footer ---
f_sp = load_font(24, "bold")
sp_text = "Powered by MLDeep Systems"
spw = text_w(draw, sp_text, f_sp)
draw.text((W - PADX - spw, 560), sp_text, font=f_sp, fill=(255, 255, 255, 220))

og.save(os.path.join(OUT, "og-image.png"), "PNG")
print("wrote og-image.png", og.size)

# ============================================================
# 2. FAVICON PNG (32) + apple-touch-icon (180)
# ============================================================
def make_icon(px):
    scale = 8
    S = px * scale
    img = diagonal_gradient(S, S, [(0.0, BERRY), (0.5, VIOLET), (1.0, BLUE)]).convert("RGBA")
    d = ImageDraw.Draw(img)
    # white bars (bar chart), coords on 100-grid
    def g(v): return round(v / 100 * S)
    bars = [(26, 52, 22), (44, 38, 36), (62, 26, 48)]  # x, y, h  (width 12)
    for (bx, by, bh) in bars:
        d.rounded_rectangle([g(bx), g(by), g(bx+12), g(by+bh)], radius=g(4), fill=WHITE)
    # rounded corners
    mask = rounded_mask((S, S), radius=g(24))
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out.resize((px, px), Image.LANCZOS)

make_icon(32).save(os.path.join(OUT, "favicon-32.png"), "PNG")
make_icon(180).save(os.path.join(OUT, "apple-touch-icon.png"), "PNG")
# also a multi-size .ico for classic browsers/tabs
ico = make_icon(64)
ico.save(os.path.join(OUT, "favicon.ico"), sizes=[(16,16),(32,32),(48,48),(64,64)])
print("wrote favicon-32.png, apple-touch-icon.png, favicon.ico")
