"""Lay out 10 business-card-size thank-you cards on a letter sheet (Avery 5371 layout)."""
from PIL import Image, ImageDraw

DPI = 300
SHEET_W, SHEET_H = int(8.5 * DPI), int(11 * DPI)   # 2550 x 3300
CARD_W, CARD_H = int(3.5 * DPI), int(2 * DPI)       # 1050 x 600
LEFT = int(0.75 * DPI)                               # 225
TOP = int(0.5 * DPI)                                 # 150

cards = [
    "card_hike.png", "card_softball.png",
    "card_robotics.png", "card_podcast.png",
    "card_cooking.png", "card_french.png",
    "card_art.png", "card_computer.png",
    "card_math.png", "card_pompom.png",
]

def fit(img):
    """Center-crop to 7:4 then resize to card size."""
    img = img.convert("RGB")
    w, h = img.size
    target = CARD_W / CARD_H
    if w / h > target:
        nw = int(h * target)
        img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / target)
        img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return img.resize((CARD_W, CARD_H), Image.LANCZOS)

sheet = Image.new("RGB", (SHEET_W, SHEET_H), "white")
draw = ImageDraw.Draw(sheet)

for i, name in enumerate(cards):
    col, row = i % 2, i // 2
    x = LEFT + col * CARD_W
    y = TOP + row * CARD_H
    sheet.paste(fit(Image.open(name)), (x, y))

# Crop marks in the margins (outside the card grid)
mark = (170, 170, 170)
GRID_R, GRID_B = LEFT + 2 * CARD_W, TOP + 5 * CARD_H
for col in range(3):  # vertical cut lines: x = LEFT, LEFT+CARD_W, GRID_R
    x = LEFT + col * CARD_W
    draw.line([(x, TOP - 110), (x, TOP - 25)], fill=mark, width=3)
    draw.line([(x, GRID_B + 25), (x, GRID_B + 110)], fill=mark, width=3)
for row in range(6):  # horizontal cut lines
    y = TOP + row * CARD_H
    draw.line([(LEFT - 190, y), (LEFT - 25, y)], fill=mark, width=3)
    draw.line([(GRID_R + 25, y), (GRID_R + 190, y)], fill=mark, width=3)

sheet.save("thank_you_cards_sheet.png", dpi=(DPI, DPI))
sheet.save("thank_you_cards_sheet.pdf", resolution=DPI)
print("done", sheet.size)
