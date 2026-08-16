import os
from urllib.parse import quote
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Product, WristSize

# ── TAXONOMY & CATEGORY MAPPING ───────────────────────────────────────────────
# Maps spreadsheet category header to (Collection, Category Display Name)
TAXONOMY = {
    "Gemstone Bracelets": ("BEST SELLERS", "Gemstone Bracelets"),
    "TREE": ("BEST SELLERS", "TREE"),
    "ANKLET": ("JEWELRY & ACCESSORIES", "ANKLET"),
    "TUMBLE STONE": ("BEST SELLERS", "TUMBLE STONE"),
    "ROUGH": ("HOME & DECOR", "ROUGH"),
    "HANGINGS": ("SPIRITUAL & HEALING", "HANGINGS"),
    "ZIBU COINS": ("HOME & DECOR", "ZIBU COINS"),
    "BRACELET CHIP": ("JEWELRY & ACCESSORIES", "BRACELET CHIP"),
    "PYRAMIDS": ("BEST SELLERS", "PYRAMIDS"),
    "SELENITE PRODUCTS": ("BEST SELLERS", "SELENITE PRODUCTS"),
    "TORTOISE": ("HOME & DECOR", "TORTOISE"),
    "PEDANTS": ("JEWELRY & ACCESSORIES", "PEDANTS"),
    "RING": ("JEWELRY & ACCESSORIES", "RING"),
    "CHIPS": ("BEST SELLERS", "CHIPS"),
}

WRIST_SIZES = [
    {"label": "XS", "cm": "13–14 cm", "inches": '5.1–5.5"'},
    {"label": "S",  "cm": "14–15 cm", "inches": '5.5–5.9"'},
    {"label": "M",  "cm": "15–17 cm", "inches": '5.9–6.7"'},
    {"label": "L",  "cm": "17–18 cm", "inches": '6.7–7.1"'},
    {"label": "XL", "cm": "18–20 cm", "inches": '7.1–7.9"'},
]

# Helper for ImageKit Cloud URLs
IK_BASE = "https://ik.imagekit.io/stoneaura/products/"

def ik_url(path: str) -> str:
    if not path or path == "*BLANK*":
        return ""
    parts = path.split("/")
    if len(parts) > 1:
        subfolder = parts[0]
        filename = "/".join(parts[1:])
        import re
        clean_subfolder = re.sub(r'[^a-zA-Z0-9_\-/]', '_', subfolder)
        clean_subfolder = re.sub(r'_+', '_', clean_subfolder).strip('_')
        return f"{IK_BASE}{clean_subfolder}/{quote(filename)}"
    return f"{IK_BASE}{quote(path)}"

# Complete 147 Product Dataset directly aligned with Spreadsheet & ImageKit
PRODUCTS_DATA = [
    # ── Gemstone Bracelets ───────────────────────────────────────────────────
    {"id": 1,  "name": "Amethyst Bracelet", "cat_key": "Gemstone Bracelets", "price": 280, "p10": 250, "p50": 190, "unit": "per piece", "img": "Amethyst Bracelet.jpg", "bead": "8mm", "feat": True},
    {"id": 2,  "name": "Carnilane Bracelet", "cat_key": "Gemstone Bracelets", "price": 200, "p10": 180, "p50": 150, "unit": "per piece", "img": "Carnilane Bracelet.webp", "bead": "8mm", "feat": True},
    {"id": 3,  "name": "Green Aventurine Bracelet", "cat_key": "Gemstone Bracelets", "price": 190, "p10": 170, "p50": 140, "unit": "per piece", "img": "Green Aventurine Bracelet.webp", "bead": "8mm", "feat": True},
    {"id": 4,  "name": "Green Jade Bracelet", "cat_key": "Gemstone Bracelets", "price": 190, "p10": 170, "p50": 140, "unit": "per piece", "img": "Green Jade Bracelet.webp", "bead": "8mm", "feat": True},
    {"id": 5,  "name": "Appetitte Bracelet", "cat_key": "Gemstone Bracelets", "price": 250, "p10": 220, "p50": 190, "unit": "per piece", "img": "", "bead": "8mm", "feat": False},
    {"id": 6,  "name": "Lapiz Bracelet", "cat_key": "Gemstone Bracelets", "price": 390, "p10": 350, "p50": 300, "unit": "per piece", "img": "Lapiz Bracelet.webp", "bead": "8mm", "feat": True},
    {"id": 7,  "name": "Sodalite Bracelet", "cat_key": "Gemstone Bracelets", "price": 190, "p10": 170, "p50": 140, "unit": "per piece", "img": "Sodalite Bracelet.jpg", "bead": "8mm", "feat": False},
    {"id": 8,  "name": "Rose Quartz Bracelet", "cat_key": "Gemstone Bracelets", "price": 190, "p10": 170, "p50": 140, "unit": "per piece", "img": "Rose Quatz Bracelet.jpg", "bead": "8mm", "feat": True},
    {"id": 9,  "name": "Calcite Bracelet", "cat_key": "Gemstone Bracelets", "price": 190, "p10": 170, "p50": 140, "unit": "per piece", "img": "Calcite Bracelet.jpg", "bead": "8mm", "feat": False},
    {"id": 10, "name": "Sunstone Dyed Bracelet", "cat_key": "Gemstone Bracelets", "price": 270, "p10": 240, "p50": 200, "unit": "per piece", "img": "Sunstone Dyed Bracelet.jpg", "bead": "8mm", "feat": False},
    {"id": 11, "name": "Sunstone Natural Bracelet", "cat_key": "Gemstone Bracelets", "price": 280, "p10": 250, "p50": 210, "unit": "per piece", "img": "Sunstone Bracelet.jpg", "bead": "8mm", "feat": True},
    {"id": 12, "name": "Turquoise Bracelet", "cat_key": "Gemstone Bracelets", "price": 190, "p10": 170, "p50": 140, "unit": "per piece", "img": "TOURQOUIS.webp", "bead": "8mm", "feat": True},
    {"id": 13, "name": "Black Obsidian Bracelet", "cat_key": "Gemstone Bracelets", "price": 180, "p10": 160, "p50": 130, "unit": "per piece", "img": "Black Obsedian Bracelet.webp", "bead": "8mm", "feat": True},
    {"id": 14, "name": "Black Obsidian 6mm Bracelet", "cat_key": "Gemstone Bracelets", "price": 160, "p10": 140, "p50": 110, "unit": "per piece", "img": "Black Obsedian 6 Mm Bracelet.webp", "bead": "6mm", "feat": False},
    {"id": 15, "name": "Black Tourmaline Bracelet", "cat_key": "Gemstone Bracelets", "price": 280, "p10": 250, "p50": 200, "unit": "per piece", "img": "black-tourmaline.png", "bead": "8mm", "feat": True},
    {"id": 16, "name": "Tiger Eye Bracelet", "cat_key": "Gemstone Bracelets", "price": 180, "p10": 160, "p50": 130, "unit": "per piece", "img": "Tiger Eye Bracelet.webp", "bead": "8mm", "feat": True},
    {"id": 17, "name": "Citrine Hydro Bracelet", "cat_key": "Gemstone Bracelets", "price": 190, "p10": 170, "p50": 140, "unit": "per piece", "img": "Citrine Hydro Bracelet.webp", "bead": "8mm", "feat": False},
    {"id": 18, "name": "Citrine Natural Bracelet", "cat_key": "Gemstone Bracelets", "price": 380, "p10": 340, "p50": 290, "unit": "per piece", "img": "Citrine Bracelet.jpg", "bead": "8mm", "feat": True},
    {"id": 19, "name": "Lava Bracelet", "cat_key": "Gemstone Bracelets", "price": 150, "p10": 130, "p50": 100, "unit": "per piece", "img": "Lava Bracelet.webp", "bead": "8mm", "feat": False},
    {"id": 20, "name": "Amazonite Bracelet", "cat_key": "Gemstone Bracelets", "price": 250, "p10": 220, "p50": 180, "unit": "per piece", "img": "Amazonite Bracelet.webp", "bead": "8mm", "feat": True},
    {"id": 21, "name": "Sulemani Akik Bracelet", "cat_key": "Gemstone Bracelets", "price": 190, "p10": 170, "p50": 140, "unit": "per piece", "img": "", "bead": "8mm", "feat": False},
    {"id": 22, "name": "Rhodonite Bracelet", "cat_key": "Gemstone Bracelets", "price": 200, "p10": 180, "p50": 150, "unit": "per piece", "img": "Rhodonite Bracelet.webp", "bead": "8mm", "feat": False},
    {"id": 23, "name": "Rhodocrosite Bracelet", "cat_key": "Gemstone Bracelets", "price": 230, "p10": 200, "p50": 170, "unit": "per piece", "img": "Rhodocrosite Bracelet.webp", "bead": "8mm", "feat": False},
    {"id": 24, "name": "Hematite Bracelet", "cat_key": "Gemstone Bracelets", "price": 150, "p10": 130, "p50": 100, "unit": "per piece", "img": "", "bead": "8mm", "feat": False},
    {"id": 25, "name": "Golden Pyrite Bracelet", "cat_key": "Gemstone Bracelets", "price": 150, "p10": 130, "p50": 100, "unit": "per piece", "img": "", "bead": "8mm", "feat": False},
    {"id": 26, "name": "Natural Pyrite Bracelet", "cat_key": "Gemstone Bracelets", "price": 280, "p10": 250, "p50": 210, "unit": "per piece", "img": "Natural Pyrite Bracelet.webp", "bead": "8mm", "feat": True},
    {"id": 27, "name": "Moonstone Bracelet", "cat_key": "Gemstone Bracelets", "price": 390, "p10": 350, "p50": 300, "unit": "per piece", "img": "Moonstone Bracelet.webp", "bead": "8mm", "feat": True},
    {"id": 28, "name": "Clear Quartz Bracelet", "cat_key": "Gemstone Bracelets", "price": 290, "p10": 260, "p50": 220, "unit": "per piece", "img": "clear-quartz.png", "bead": "8mm", "feat": False},
    {"id": 29, "name": "Red Jasper Bracelet", "cat_key": "Gemstone Bracelets", "price": 190, "p10": 170, "p50": 140, "unit": "per piece", "img": "Red Jasper Bracelet.jpg", "bead": "8mm", "feat": True},
    {"id": 30, "name": "Yellow Cat-Eye Bracelet", "cat_key": "Gemstone Bracelets", "price": 290, "p10": 260, "p50": 210, "unit": "per piece", "img": "", "bead": "8mm", "feat": False},
    {"id": 31, "name": "Black Cat Eye Bracelet", "cat_key": "Gemstone Bracelets", "price": 460, "p10": 420, "p50": 390, "unit": "per piece", "img": "", "bead": "8mm", "feat": False},
    {"id": 32, "name": "Karungilini Mala", "cat_key": "Gemstone Bracelets", "price": 250, "p10": 220, "p50": 180, "unit": "per piece", "img": "", "bead": "8mm", "feat": False},

    # ── TREE Category ────────────────────────────────────────────────────────
    {"id": 33, "name": "Seven Chakra Tree", "cat_key": "TREE", "price": 350, "p10": 295, "p50": 255, "unit": "per piece", "img": "tree photos/Seven Charka Tree.jpg", "feat": True},
    {"id": 34, "name": "Money Magnet Tree", "cat_key": "TREE", "price": 320, "p10": 290, "p50": 275, "unit": "per piece", "img": "tree photos/Money Magnet Tree.png", "feat": True},
    {"id": 35, "name": "Rose Quartz Tree", "cat_key": "TREE", "price": 360, "p10": 295, "p50": 250, "unit": "per piece", "img": "tree photos/Rose Quatz Tree.jpg", "feat": True},
    {"id": 36, "name": "Evil Eye Tree", "cat_key": "TREE", "price": 350, "p10": 300, "p50": 260, "unit": "per piece", "img": "tree photos/Pyrite cluster tree.jpg", "feat": False},

    # ── ANKLET Category ──────────────────────────────────────────────────────
    {"id": 37, "name": "Dhanyog Anklet", "cat_key": "ANKLET", "price": 180, "unit": "single/pair", "size_info": "180 SINGLE PC / 220 PAIR", "img": "anklet/Dhanyog Anklet.jpeg", "feat": True},
    {"id": 38, "name": "Pyrite Anklet", "cat_key": "ANKLET", "price": 180, "unit": "single/pair", "size_info": "180 SINGLE PC / 220 PAIR", "img": "anklet/Pyrite Anklet.jpeg", "feat": True},
    {"id": 39, "name": "Triple Protection Anklet", "cat_key": "ANKLET", "price": 180, "unit": "single/pair", "size_info": "180 SINGLE PC / 220 PAIR", "img": "anklet/Triple Protection Anklet.jpeg", "feat": True},

    # ── TUMBLE STONE Category ────────────────────────────────────────────────
    {"id": 40, "name": "Rose Tumble Stone", "cat_key": "TUMBLE STONE", "price": 650, "unit": "per kg", "img": "tumble stones/Rose Tumble Stone.jpeg", "feat": True},
    {"id": 41, "name": "Amethyst Tumble Stone", "cat_key": "TUMBLE STONE", "price": 650, "unit": "per kg", "img": "tumble stones/Amethyst Tumble Stone.jpeg", "feat": True},
    {"id": 42, "name": "Selenite Tumble Stone", "cat_key": "TUMBLE STONE", "price": 700, "unit": "per kg", "img": "", "feat": False},
    {"id": 43, "name": "Clear Quartz Tumble Stone", "cat_key": "TUMBLE STONE", "price": 650, "unit": "per kg", "img": "", "feat": False},
    {"id": 44, "name": "Black Obsidian Tumble Stone", "cat_key": "TUMBLE STONE", "price": 650, "unit": "per kg", "img": "", "feat": False},
    {"id": 45, "name": "Black Tourmaline Tumble Stone", "cat_key": "TUMBLE STONE", "price": 750, "unit": "per kg", "img": "", "feat": False},
    {"id": 46, "name": "Red Jasper Tumble Stone", "cat_key": "TUMBLE STONE", "price": 500, "unit": "per kg", "img": "", "feat": False},
    {"id": 47, "name": "Green Aventurine Tumble Stone", "cat_key": "TUMBLE STONE", "price": 650, "unit": "per kg", "img": "tumble stones/Green Aventurine Tumble Stone.jpeg", "feat": False},
    {"id": 48, "name": "Green Jade Tumble Stone", "cat_key": "TUMBLE STONE", "price": 650, "unit": "per kg", "img": "tumble stones/Green Jade Tumble Stone.jpeg", "feat": False},
    {"id": 49, "name": "Tiger Eye Tumble Stone", "cat_key": "TUMBLE STONE", "price": 750, "unit": "per kg", "img": "tumble stones/Tiger Eye Tumble Stone.jpeg", "feat": True},
    {"id": 50, "name": "Pyrite Tumble Stone", "cat_key": "TUMBLE STONE", "price": 780, "unit": "per kg", "img": "", "feat": False},
    {"id": 51, "name": "Multi Flourite Tumble Stone", "cat_key": "TUMBLE STONE", "price": 1480, "unit": "per kg", "img": "", "feat": False},
    {"id": 52, "name": "Citrine Natural Tumble Stone", "cat_key": "TUMBLE STONE", "price": 1990, "unit": "per kg", "img": "tumble stones/Citrine Natural Tumble Stone.jpeg", "feat": True},
    {"id": 53, "name": "Citrine Hydro Tumble Stone", "cat_key": "TUMBLE STONE", "price": 3680, "unit": "per kg", "img": "tumble stones/Citrine Hydro Tumble Stone.jpeg", "feat": False},
    {"id": 54, "name": "Aquamarine Tumble Stone", "cat_key": "TUMBLE STONE", "price": 1200, "unit": "per kg", "img": "", "feat": False},
    {"id": 55, "name": "Carnilane Tumble Stone", "cat_key": "TUMBLE STONE", "price": 750, "unit": "per kg", "img": "tumble stones/Carnilane Tumble Stone.jpeg", "feat": False},
    {"id": 56, "name": "Dalmatian Tumble Stone", "cat_key": "TUMBLE STONE", "price": 650, "unit": "per kg", "img": "", "feat": False},
    {"id": 57, "name": "Sodalite Tumble Stone", "cat_key": "TUMBLE STONE", "price": 650, "unit": "per kg", "img": "tumble stones/Sodalite Tumble Stone.jpeg", "feat": False},
    {"id": 58, "name": "Lapis Lazuli Tumble Stone", "cat_key": "TUMBLE STONE", "price": 850, "unit": "per kg", "img": "tumble stones/lapiz lazuli tumble stone .jpeg", "feat": False},
    {"id": 59, "name": "Hematite Tumble Stone", "cat_key": "TUMBLE STONE", "price": 500, "unit": "per kg", "img": "", "feat": False},
    {"id": 60, "name": "Labradorite Tumble Stone", "cat_key": "TUMBLE STONE", "price": 750, "unit": "per kg", "img": "", "feat": False},

    # ── ROUGH Category ───────────────────────────────────────────────────────
    {"id": 64, "name": "Multi Flourite Rough Stone", "cat_key": "ROUGH", "price": 270, "unit": "per kg", "img": "", "feat": False},
    {"id": 65, "name": "Carnilane Rough Stone", "cat_key": "ROUGH", "price": 300, "unit": "per kg", "img": "", "feat": False},
    {"id": 66, "name": "Black Tourmaline Rough Stone", "cat_key": "ROUGH", "price": 260, "unit": "per kg", "img": "", "feat": False},
    {"id": 67, "name": "Green Aventurine Rough Stone", "cat_key": "ROUGH", "price": 300, "unit": "per kg", "img": "", "feat": False},
    {"id": 68, "name": "Citrine Natural Rough Stone", "cat_key": "ROUGH", "price": 850, "unit": "per kg", "img": "", "feat": False},
    {"id": 69, "name": "Amethyst Rough Stone", "cat_key": "ROUGH", "price": 450, "unit": "per kg", "img": "", "feat": False},
    {"id": 70, "name": "Rose Quartz Rough Stone", "cat_key": "ROUGH", "price": 280, "unit": "per kg", "img": "", "feat": False},

    # ── HANGINGS Category ────────────────────────────────────────────────────
    {"id": 71, "name": "Seven Chakra Tumble with Evil Hanging (Dori)", "cat_key": "HANGINGS", "price": 190, "unit": "per piece", "img": "", "feat": False},
    {"id": 72, "name": "Seven Chakra Tumble with Chip Hanging", "cat_key": "HANGINGS", "price": 190, "unit": "per piece", "img": "", "feat": False},
    {"id": 73, "name": "Pyrite Cluster Evil Eye Hanging", "cat_key": "HANGINGS", "price": 190, "unit": "per piece", "img": "", "feat": True},
    {"id": 74, "name": "Metal Pyrite Cluster Hanging", "cat_key": "HANGINGS", "price": 190, "unit": "per piece", "img": "", "feat": False},
    {"id": 75, "name": "Clear Quartz Tumble with Evil Eye Hanging", "cat_key": "HANGINGS", "price": 230, "unit": "per piece", "img": "", "feat": False},
    {"id": 76, "name": "Metal Seven Chakra 21 Beads Hanging", "cat_key": "HANGINGS", "price": 160, "unit": "per piece", "img": "", "feat": False},
    {"id": 77, "name": "Metal Seven Chakra 15 Beads (Dori)", "cat_key": "HANGINGS", "price": 150, "unit": "per piece", "img": "", "feat": False},
    {"id": 78, "name": "3 Evil Eye with Pyrite Cluster Hanging", "cat_key": "HANGINGS", "price": 160, "unit": "per piece", "img": "", "feat": True},
    {"id": 79, "name": "Black Tourmaline & Selenite with Evil Eye (Dori)", "cat_key": "HANGINGS", "price": 180, "unit": "per piece", "img": "", "feat": False},
    {"id": 80, "name": "Black Tourmaline (Dori)", "cat_key": "HANGINGS", "price": 110, "unit": "per piece", "img": "", "feat": False},
    {"id": 81, "name": "Selenite Hanging", "cat_key": "HANGINGS", "price": 110, "unit": "per piece", "img": "", "feat": False},
    {"id": 82, "name": "Black Tourmaline with Evil Eye (Dori)", "cat_key": "HANGINGS", "price": 120, "unit": "per piece", "img": "", "feat": False},
    {"id": 83, "name": "Selenite with Evil Eye", "cat_key": "HANGINGS", "price": 120, "unit": "per piece", "img": "", "feat": False},
    {"id": 84, "name": "Pyrite Cluster Key Chain 3 PC", "cat_key": "HANGINGS", "price": 110, "unit": "per piece", "img": "", "feat": False},
    {"id": 85, "name": "Pyrite Cluster Key Chain 1 PC", "cat_key": "HANGINGS", "price": 110, "unit": "per piece", "img": "", "feat": False},

    # ── ZIBU COINS Category ──────────────────────────────────────────────────
    {"id": 86, "name": "Green Jade Zibu Coin", "cat_key": "ZIBU COINS", "price": 150, "unit": "per piece", "img": "zibu coins/Green Jade Zibu Coin.jpeg", "feat": True},
    {"id": 87, "name": "Pyrite Zibu Coin", "cat_key": "ZIBU COINS", "price": 150, "unit": "per piece", "img": "zibu coins/Pyrite Zibu Coin.jpeg", "feat": True},
    {"id": 88, "name": "Rose Quartz Zibu Coin", "cat_key": "ZIBU COINS", "price": 150, "unit": "per piece", "img": "zibu coins/Rose Zibu Coin.jpeg", "feat": True},
    {"id": 89, "name": "Seven Chakra Zibu Coin", "cat_key": "ZIBU COINS", "price": 150, "unit": "per piece", "img": "zibu coins/Seven Chakra Zibu Coin.jpeg", "feat": True},

    # ── BRACELET CHIP Category ───────────────────────────────────────────────
    {"id": 90, "name": "7 Chakra Chip Bracelet", "cat_key": "BRACELET CHIP", "price": 250, "unit": "per piece", "img": "", "feat": False},
    {"id": 91, "name": "Dhanyog Chip Bracelet", "cat_key": "BRACELET CHIP", "price": 250, "unit": "per piece", "img": "", "feat": False},
    {"id": 92, "name": "Money Magnet Chip Bracelet", "cat_key": "BRACELET CHIP", "price": 250, "unit": "per piece", "img": "Money Magnet.jpg", "feat": True},
    {"id": 93, "name": "Carnilane Chip Bracelet", "cat_key": "BRACELET CHIP", "price": 250, "unit": "per piece", "img": "Carnilane.webp", "feat": False},
    {"id": 94, "name": "Rose Chip Bracelet", "cat_key": "BRACELET CHIP", "price": 250, "unit": "per piece", "img": "Rose.jpg", "feat": True},
    {"id": 95, "name": "Amethyst Chip Bracelet", "cat_key": "BRACELET CHIP", "price": 250, "unit": "per piece", "img": "Amethyst.jpg", "feat": True},

    # ── PYRAMIDS Category ────────────────────────────────────────────────────
    {"id": 96, "name": "Citrine 3 Inch Pyramid", "cat_key": "PYRAMIDS", "price": 250, "unit": "per piece", "img": "", "feat": False},
    {"id": 97, "name": "Laxmi Shree Yantra 4 Inch Pyramid", "cat_key": "PYRAMIDS", "price": 290, "unit": "per piece", "img": "", "feat": True},
    {"id": 98, "name": "Pyrite Laxmi Pyramid", "cat_key": "PYRAMIDS", "price": 250, "unit": "per piece", "img": "", "feat": True},
    {"id": 99, "name": "Money Magnet Pyramid", "cat_key": "PYRAMIDS", "price": 250, "unit": "per piece", "img": "", "feat": True},
    {"id": 100, "name": "Black Tourmaline Pyramid", "cat_key": "PYRAMIDS", "price": 250, "unit": "per piece", "img": "", "feat": False},

    # ── SELENITE PRODUCTS Category ───────────────────────────────────────────
    {"id": 101, "name": "Selenite Round Shape Plate Plain", "cat_key": "SELENITE PRODUCTS", "price": 180, "unit": "per piece", "img": "selenite charging plates and lamp/PLAIN ROUND SHAPE SELENITE PLATE.jpeg", "feat": False},
    {"id": 102, "name": "Selenite Round Shape Plate Carving", "cat_key": "SELENITE PRODUCTS", "price": 220, "unit": "per piece", "img": "selenite charging plates and lamp/Selenite Round Shape Plate Carving.jpeg", "feat": True},
    {"id": 103, "name": "Selenite Round Bowl", "cat_key": "SELENITE PRODUCTS", "price": 450, "unit": "per piece", "img": "", "feat": False},
    {"id": 104, "name": "Selenite Star Moon Bowl", "cat_key": "SELENITE PRODUCTS", "price": 460, "unit": "per piece", "img": "", "feat": False},
    {"id": 105, "name": "Selenite Any Shape Bowl 3 Inch", "cat_key": "SELENITE PRODUCTS", "price": 460, "unit": "per piece", "img": "", "feat": False},
    {"id": 106, "name": "Selenite Lamp (Owl)", "cat_key": "SELENITE PRODUCTS", "price": 220, "unit": "per piece", "img": "", "feat": False},
    {"id": 107, "name": "Selenite Lamp (Square)", "cat_key": "SELENITE PRODUCTS", "price": 220, "unit": "per piece", "img": "", "feat": False},
    {"id": 108, "name": "Seven Chakra Selenite Lamp", "cat_key": "SELENITE PRODUCTS", "price": 280, "unit": "per piece", "img": "", "feat": False},
    {"id": 109, "name": "Citrine Selenite Lamp", "cat_key": "SELENITE PRODUCTS", "price": 300, "unit": "per piece", "img": "", "feat": False},

    # ── TORTOISE Category ────────────────────────────────────────────────────
    {"id": 110, "name": "Money Magnet Tortoise", "cat_key": "TORTOISE", "price": 250, "unit": "per piece", "img": "", "feat": False},
    {"id": 111, "name": "Pyrite Tortoise", "cat_key": "TORTOISE", "price": 250, "unit": "per piece", "img": "", "feat": True},
    {"id": 112, "name": "Seven Chakra Tortoise", "cat_key": "TORTOISE", "price": 250, "unit": "per piece", "img": "", "feat": False},

    # ── PEDANTS Category ─────────────────────────────────────────────────────
    {"id": 113, "name": "Rose Quartz Pendant", "cat_key": "PEDANTS", "price": 130, "unit": "per piece", "img": "", "feat": False},
    {"id": 114, "name": "Amethyst Pendant", "cat_key": "PEDANTS", "price": 130, "unit": "per piece", "img": "", "feat": False},
    {"id": 115, "name": "Green Aventurine Pendant", "cat_key": "PEDANTS", "price": 130, "unit": "per piece", "img": "", "feat": False},
    {"id": 116, "name": "Clear Quartz Pendant", "cat_key": "PEDANTS", "price": 130, "unit": "per piece", "img": "", "feat": False},
    {"id": 117, "name": "Tiger Eye Pendant", "cat_key": "PEDANTS", "price": 130, "unit": "per piece", "img": "", "feat": False},
    {"id": 118, "name": "Red Jasper Pendant", "cat_key": "PEDANTS", "price": 130, "unit": "per piece", "img": "", "feat": False},
    {"id": 119, "name": "Opal Pendant", "cat_key": "PEDANTS", "price": 130, "unit": "per piece", "img": "", "feat": False},
    {"id": 120, "name": "Lapis Lazuli Pendant", "cat_key": "PEDANTS", "price": 130, "unit": "per piece", "img": "", "feat": False},
    {"id": 121, "name": "Pencil Cap Pendant Single Point", "cat_key": "PEDANTS", "price": 130, "unit": "per piece", "img": "", "feat": False},

    # ── RING Category ────────────────────────────────────────────────────────
    {"id": 129, "name": "Citrine Ring", "cat_key": "RING", "price": 150, "unit": "per piece", "img": "", "feat": False},
    {"id": 130, "name": "Amethyst Ring", "cat_key": "RING", "price": 150, "unit": "per piece", "img": "", "feat": False},
    {"id": 131, "name": "Pyrite Ring", "cat_key": "RING", "price": 150, "unit": "per piece", "img": "", "feat": False},
    {"id": 132, "name": "Black Obsidian Ring", "cat_key": "RING", "price": 150, "unit": "per piece", "img": "", "feat": False},
    {"id": 133, "name": "Tiger Eye Ring", "cat_key": "RING", "price": 150, "unit": "per piece", "img": "", "feat": False},

    # ── CHIPS Category ───────────────────────────────────────────────────────
    {"id": 134, "name": "Amethyst Chips", "cat_key": "CHIPS", "price": 170, "unit": "per kg", "img": "chips/Amethyst Chips.jpeg", "feat": True},
    {"id": 135, "name": "Clear Quartz Chips", "cat_key": "CHIPS", "price": 170, "unit": "per kg", "img": "chips/Clear Quatz Chips.jpeg", "feat": False},
    {"id": 136, "name": "Rose Quartz Chips", "cat_key": "CHIPS", "price": 170, "unit": "per kg", "img": "", "feat": False},
    {"id": 137, "name": "Garnet Chips", "cat_key": "CHIPS", "price": 210, "unit": "per kg", "img": "chips/Garnet Chips.jpeg", "feat": False},
    {"id": 138, "name": "Rainbow Moonstone Chips", "cat_key": "CHIPS", "price": 250, "unit": "per kg", "img": "chips/Rainbow Moonstone Chips.jpeg", "feat": True},
    {"id": 139, "name": "Amazonite Chips", "cat_key": "CHIPS", "price": 180, "unit": "per kg", "img": "chips/Amazonite Chips.jpeg", "feat": False},
    {"id": 140, "name": "Green Jade Chips", "cat_key": "CHIPS", "price": 180, "unit": "per kg", "img": "chips/Green Jade Chips.jpeg", "feat": False},
    {"id": 141, "name": "Green Aventurine Chips", "cat_key": "CHIPS", "price": 180, "unit": "per kg", "img": "chips/Green Aventurin E Chips.jpeg", "feat": False},
    {"id": 142, "name": "Sunstone Chips", "cat_key": "CHIPS", "price": 180, "unit": "per kg", "img": "", "feat": False},
    {"id": 143, "name": "Black Agate Chips", "cat_key": "CHIPS", "price": 160, "unit": "per kg", "img": "chips/Black Agate Chips.jpeg", "feat": False},
    {"id": 144, "name": "Carnilane Chips", "cat_key": "CHIPS", "price": 170, "unit": "per kg", "img": "chips/Carnilane Chips.jpeg", "feat": False},
    {"id": 145, "name": "White Agate Chips", "cat_key": "CHIPS", "price": 160, "unit": "per kg", "img": "chips/White Agate Chips.jpeg", "feat": False},
    {"id": 146, "name": "Red Jasper Chips", "cat_key": "CHIPS", "price": 170, "unit": "per kg", "img": "", "feat": False},
    {"id": 147, "name": "Yellow Aventurine Chips", "cat_key": "CHIPS", "price": 180, "unit": "per kg", "img": "chips/Yello Aventurine Chips.jpeg", "feat": False},
    {"id": 148, "name": "Lapis Lazuli Chips", "cat_key": "CHIPS", "price": 410, "unit": "per kg", "img": "chips/Lapiz Chips.jpeg", "feat": True},
]

class Command(BaseCommand):
    help = "Seed database with exact product taxonomy, names, prices, categories, and ImageKit links from spreadsheet."

    def handle(self, *args, **options):
        # 1. Clean up ALL existing products
        Product.objects.all().delete()
        self.stdout.write(self.style.WARNING("Cleared all products from the database."))

        # 2. Seed wrist sizes
        WristSize.objects.all().delete()
        WristSize.objects.bulk_create([WristSize(**ws) for ws in WRIST_SIZES])
        self.stdout.write(self.style.SUCCESS(f"  [OK]  {len(WRIST_SIZES)} wrist sizes seeded."))

        # 3. Seed Products
        created = 0
        for item in PRODUCTS_DATA:
            coll, cat = TAXONOMY.get(item["cat_key"], ("BEST SELLERS", item["cat_key"]))
            
            slug = slugify(item["name"])
            base, n = slug, 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1

            stone_type = item["name"].replace(" Bracelet", "").replace(" Anklet", "").replace(" Tree", "").replace(" Tumble Stone", "").replace(" Rough Stone", "").replace(" Zibu Coin", "").replace(" Chip Bracelet", "").replace(" Chips", "").replace(" Pyramid", "").replace(" Pendant", "").replace(" Ring", "").strip()

            img_url = ik_url(item["img"]) if item.get("img") else f"https://placehold.co/480x480/f5f0e8/c9a84c?text={quote(item['name'])}"

            wa_link = f"https://wa.me/919104139899?text=Hi%2C%20I%20am%20interested%20in%20{quote(item['name'])}"

            Product.objects.create(
                id=item["id"],
                name=item["name"],
                slug=slug,
                price=item.get("price"),
                price_10pc=item.get("p10"),
                price_50pc=item.get("p50"),
                price_unit=item.get("unit", "per piece"),
                stone_type=stone_type,
                color="",
                material="Natural Gemstone",
                bead_size=item.get("bead", ""),
                size_info=item.get("size_info", ""),
                gender="Unisex",
                collection=coll,
                category=cat,
                image_url=img_url,
                whatsapp_link=wa_link,
                is_featured=item.get("feat", False),
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {created} products with exact categories and ImageKit links!"))
