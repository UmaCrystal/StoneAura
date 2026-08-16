import os
from urllib.parse import quote
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Product, WristSize

# ── TAXONOMY & CATEGORY MAPPING ───────────────────────────────────────────────
# Maps spreadsheet category key -> (Collection, DB Category)
TAXONOMY = {
    "Gemstone Bracelets":  ("BEST SELLERS",          "Gemstone Bracelets"),
    "Gemstone Tree":       ("BEST SELLERS",          "TREE"),
    "ANKLET":              ("JEWELRY & ACCESSORIES", "ANKLET"),
    "Tumbled Stones":      ("BEST SELLERS",          "TUMBLE STONE"),
    "Rough Stone":         ("HOME & DECOR",          "ROUGH"),
    "HANGINGS":            ("SPIRITUAL & HEALING",   "HANGINGS"),
    "Zibu Coin":           ("HOME & DECOR",          "ZIBU COINS"),
    "BRACELET CHIP":       ("JEWELRY & ACCESSORIES", "BRACELET CHIP"),
    "Orgone Pyramid":      ("BEST SELLERS",          "PYRAMIDS"),
    "Selenite Stone":      ("BEST SELLERS",          "SELENITE PRODUCTS"),
    "TORTOISE":            ("HOME & DECOR",          "TORTOISE"),
    "Gemstone Pendant":    ("JEWELRY & ACCESSORIES", "PEDANTS"),
    "RING":                ("JEWELRY & ACCESSORIES", "RING"),
    "CHIPS":               ("BEST SELLERS",          "CHIPS"),
}

WRIST_SIZES = [
    {"label": "XS", "cm": "13–14 cm", "inches": '5.1–5.5"'},
    {"label": "S",  "cm": "14–15 cm", "inches": '5.5–5.9"'},
    {"label": "M",  "cm": "15–17 cm", "inches": '5.9–6.7"'},
    {"label": "L",  "cm": "17–18 cm", "inches": '6.7–7.1"'},
    {"label": "XL", "cm": "18–20 cm", "inches": '7.1–7.9"'},
]

# ── ImageKit Cloud URL Builder ────────────────────────────────────────────────
IK_BASE = "https://ik.imagekit.io/stoneaura/products/"

# ImageKit folder names (as uploaded — spaces replaced with underscores)
IK_FOLDERS = {
    "anklet":    "anklet",
    "bead_lines": "bead_lines",
    "chips":     "chips",
    "selenite":  "selenite_charging_plates_and_lamp",
    "tree":      "tree_photos",
    "tumble":    "tumble_stones",
    "zibu":      "zibu_coins",
}

def ik_url(folder_key, filename):
    """Build ImageKit URL. folder_key=None means root products/ folder."""
    if not filename:
        return ""
    if folder_key:
        folder = IK_FOLDERS[folder_key]
        return f"{IK_BASE}{folder}/{quote(filename)}"
    return f"{IK_BASE}{quote(filename)}"

# ── Complete Product Dataset — Exactly matching spreadsheet rows 1–148 ────────
# Fields:
#   id     = spreadsheet row number
#   name   = display name
#   cat    = TAXONOMY key
#   price  = Price 1 (1PC / 1KG / Single)    — None if "-"
#   p10    = Price 2 (10PC / Pair)            — None if "-"
#   p50    = Price 3 (50PC)                   — None if "-"
#   unit   = "per piece" / "per kg" / "single/pair"
#   img    = (folder_key, filename) or ("", "") if no image
#   bead   = bead size (only for per-piece bracelets)
#   feat   = is_featured flag
#   size_info = extra size/pricing info string

PRODUCTS_DATA = [
    # ══════════════════════════════════════════════════════════════════════════
    # GEMSTONE BRACELETS (rows 1–32) — Per PC, bead 8mm
    # Images in products/ root folder on ImageKit
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 1,  "name": "Amethyst Bracelet",           "cat": "Gemstone Bracelets", "price": 280,  "p10": 230,  "p50": 180,  "unit": "per piece", "img": (None, "AMETHYST_BRACELET_1.webp"),                    "bead": "8mm", "feat": True},
    {"id": 2,  "name": "Carnilane Bracelet",          "cat": "Gemstone Bracelets", "price": 200,  "p10": 150,  "p50": 120,  "unit": "per piece", "img": (None, "CARNILANE.webp"),                              "bead": "8mm", "feat": True},
    {"id": 3,  "name": "Green Aventurine Bracelet",   "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "GREEN AVENTURINE.webp"),                      "bead": "8mm", "feat": True},
    {"id": 4,  "name": "Green Jade Bracelet",         "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "GREEN JADE.webp"),                            "bead": "8mm", "feat": True},
    {"id": 5,  "name": "Appetitte Bracelet",          "cat": "Gemstone Bracelets", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},
    {"id": 6,  "name": "Lapiz Bracelet",              "cat": "Gemstone Bracelets", "price": 390,  "p10": 320,  "p50": 250,  "unit": "per piece", "img": (None, "lapiz.webp"),                                 "bead": "8mm", "feat": True},
    {"id": 7,  "name": "Sodalite Bracelet",           "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "sodalite-gemstones-bracelet-1.jpg"),           "bead": "8mm", "feat": False},
    {"id": 8,  "name": "Rose Quartz Bracelet",        "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "ROSE QUATZ IM 1.jpg"),                        "bead": "8mm", "feat": True},
    {"id": 9,  "name": "Calcite Bracelet",            "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "CALCITE.webp"),                               "bead": "8mm", "feat": False},
    {"id": 10, "name": "Sunstone Dyed Bracelet",      "cat": "Gemstone Bracelets", "price": 270,  "p10": 150,  "p50": 130,  "unit": "per piece", "img": (None, "sunstone.jpg"),                               "bead": "8mm", "feat": False},
    {"id": 11, "name": "Sunstone Natural Bracelet",   "cat": "Gemstone Bracelets", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, "sunstone.jpg"),                               "bead": "8mm", "feat": False},
    {"id": 12, "name": "Turquoise Bracelet",          "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "TOURQOUIS.webp"),                             "bead": "8mm", "feat": True},
    {"id": 13, "name": "Black Obsidian Bracelet",     "cat": "Gemstone Bracelets", "price": 180,  "p10": 145,  "p50": 115,  "unit": "per piece", "img": (None, "BLACK OBSEDIAN.webp"),                        "bead": "8mm", "feat": True},
    {"id": 14, "name": "Black Obsidian 8mm Bracelet", "cat": "Gemstone Bracelets", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, "BLACK OBSEDIAN.webp"),                        "bead": "8mm", "feat": False},
    {"id": 15, "name": "Black Tourmaline Bracelet",   "cat": "Gemstone Bracelets", "price": 280,  "p10": 230,  "p50": 180,  "unit": "per piece", "img": (None, "BLACK TOURMALINE.webp"),                      "bead": "8mm", "feat": True},
    {"id": 16, "name": "Tiger Eye Bracelet",          "cat": "Gemstone Bracelets", "price": 180,  "p10": 145,  "p50": 115,  "unit": "per piece", "img": (None, "TIGER_EYE.webp"),                             "bead": "8mm", "feat": True},
    {"id": 17, "name": "Citrine Hydro Bracelet",      "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "CITRINE HYDRO.webp"),                         "bead": "8mm", "feat": False},
    {"id": 18, "name": "Citrine Natural Bracelet",    "cat": "Gemstone Bracelets", "price": 380,  "p10": 290,  "p50": 250,  "unit": "per piece", "img": (None, "CITRINE.jpg"),                                "bead": "8mm", "feat": True},
    {"id": 19, "name": "Lava Bracelet",               "cat": "Gemstone Bracelets", "price": 150,  "p10": 110,  "p50": 85,   "unit": "per piece", "img": (None, "lava bracelet.webp"),                         "bead": "8mm", "feat": False},
    {"id": 20, "name": "Amazonite Bracelet",          "cat": "Gemstone Bracelets", "price": 250,  "p10": 195,  "p50": 150,  "unit": "per piece", "img": (None, "AMAZONITE.webp"),                             "bead": "8mm", "feat": True},
    {"id": 21, "name": "Sulemani Akik Bracelet",      "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},
    {"id": 22, "name": "Rhodonite Bracelet",          "cat": "Gemstone Bracelets", "price": 200,  "p10": 170,  "p50": 150,  "unit": "per piece", "img": (None, "RHODONITE_001fd9ac-08a2-4d42-9b10-30a73fbc9134.webp"), "bead": "8mm", "feat": False},
    {"id": 23, "name": "Rhodocrosite Bracelet",       "cat": "Gemstone Bracelets", "price": 230,  "p10": 180,  "p50": 160,  "unit": "per piece", "img": (None, "RHODOCROSITE_00ac6fb4-328e-467b-aa89-ec1a5213876b.webp"), "bead": "8mm", "feat": False},
    {"id": 24, "name": "Hematite Bracelet",           "cat": "Gemstone Bracelets", "price": 150,  "p10": 110,  "p50": 90,   "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},
    {"id": 25, "name": "Golden Pyrite Bracelet",      "cat": "Gemstone Bracelets", "price": 150,  "p10": 110,  "p50": 90,   "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},
    {"id": 26, "name": "Natural Pyrite Bracelet",     "cat": "Gemstone Bracelets", "price": 280,  "p10": 240,  "p50": 195,  "unit": "per piece", "img": (None, "NATURAL_PYRITE.webp"),                        "bead": "8mm", "feat": True},
    {"id": 27, "name": "Moonstone Bracelet",          "cat": "Gemstone Bracelets", "price": 390,  "p10": 320,  "p50": 250,  "unit": "per piece", "img": (None, "moon stone.jpg"),                             "bead": "8mm", "feat": True},
    {"id": 28, "name": "Clear Quartz Bracelet",       "cat": "Gemstone Bracelets", "price": 290,  "p10": 240,  "p50": 190,  "unit": "per piece", "img": (None, "CLEAR QUATZ.webp"),                           "bead": "8mm", "feat": False},
    {"id": 29, "name": "Red Jasper Bracelet",         "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "RED JASPER_.jpg"),                            "bead": "8mm", "feat": True},
    {"id": 30, "name": "Yellow Cat-Eye Bracelet",     "cat": "Gemstone Bracelets", "price": 290,  "p10": 240,  "p50": 190,  "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},
    {"id": 31, "name": "Black Cat Eye Bracelet",      "cat": "Gemstone Bracelets", "price": 460,  "p10": 420,  "p50": 390,  "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},
    {"id": 32, "name": "Karungilini Mala",            "cat": "Gemstone Bracelets", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},

    # ══════════════════════════════════════════════════════════════════════════
    # GEMSTONE TREE (rows 33–36) — Per PC, no bead
    # Images in products/tree_photos/ on ImageKit
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 33, "name": "Seven Chakra Tree",   "cat": "Gemstone Tree", "price": 350,  "p10": 295,  "p50": 255,  "unit": "per piece", "img": ("tree", "seven chakra tree 300 chips.jpg"),   "feat": True},
    {"id": 34, "name": "Money Magnet Tree",   "cat": "Gemstone Tree", "price": 320,  "p10": 290,  "p50": 275,  "unit": "per piece", "img": ("tree", "money magnet tree 300 chips.png"),   "feat": True},
    {"id": 35, "name": "Rose Quartz Tree",    "cat": "Gemstone Tree", "price": 360,  "p10": 295,  "p50": 250,  "unit": "per piece", "img": ("tree", "rose quatz tree 300 chips.jpg"),     "feat": True},
    {"id": 36, "name": "Evil Eye Tree",       "cat": "Gemstone Tree", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": ("tree", "Pyrite cluster tree.jpg"),            "feat": False},

    # ══════════════════════════════════════════════════════════════════════════
    # ANKLET (rows 37–39) — Single / Pair, no bead
    # Images in products/anklet/ on ImageKit
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 37, "name": "Dhanyog Anklet",            "cat": "ANKLET", "price": 180, "p10": 220, "p50": None, "unit": "single/pair", "img": ("anklet", "money magnet anklet .jpeg"),          "feat": True,  "size_info": "180 Single / 220 Pair"},
    {"id": 38, "name": "Pyrite Anklet",             "cat": "ANKLET", "price": 180, "p10": 220, "p50": None, "unit": "single/pair", "img": ("anklet", "pyrite anklet .jpeg"),                "feat": True,  "size_info": "180 Single / 220 Pair"},
    {"id": 39, "name": "Triple Protection Anklet",  "cat": "ANKLET", "price": 180, "p10": 220, "p50": None, "unit": "single/pair", "img": ("anklet", "triple protection anklet .jpeg"),    "feat": True,  "size_info": "180 Single / 220 Pair"},

    # ══════════════════════════════════════════════════════════════════════════
    # TUMBLED STONES (rows 40–63) — Per KG, NO bead size
    # Images in products/tumble_stones/ on ImageKit
    # Note: rows 58-60 and 61-63 have duplicates (Lapis, Hematite, Labradorite)
    # Keeping unique names only — using last price if duplicated
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 40, "name": "Rose Tumble Stone",             "cat": "Tumbled Stones", "price": 650,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "rose quatz tumble stone.jpeg"),              "feat": True},
    {"id": 41, "name": "Amethyst Tumble Stone",         "cat": "Tumbled Stones", "price": 650,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "amethyst tumble stone .jpeg"),               "feat": True},
    {"id": 42, "name": "Selenite Tumble Stone",         "cat": "Tumbled Stones", "price": 700,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 43, "name": "Clear Quartz Tumble Stone",     "cat": "Tumbled Stones", "price": 650,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 44, "name": "Black Obsidian Tumble Stone",   "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 45, "name": "Black Tourmaline Tumble Stone", "cat": "Tumbled Stones", "price": 750,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 46, "name": "Red Jasper Tumble Stone",       "cat": "Tumbled Stones", "price": 500,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 47, "name": "Green Aventurine Tumble Stone", "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "green aventurine tumble stone .jpeg"),       "feat": False},
    {"id": 48, "name": "Green Jade Tumble Stone",       "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "green jade tumble stone .jpeg"),             "feat": False},
    {"id": 49, "name": "Tiger Eye Tumble Stone",        "cat": "Tumbled Stones", "price": 750,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "tiger eye tumble stone .jpeg"),              "feat": True},
    {"id": 50, "name": "Pyrite Tumble Stone",           "cat": "Tumbled Stones", "price": 780,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 51, "name": "Multi Flourite Tumble Stone",   "cat": "Tumbled Stones", "price": 1480, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 52, "name": "Citrine Natural Tumble Stone",  "cat": "Tumbled Stones", "price": 1990, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "citrine natural tumble stone .jpeg"),        "feat": True},
    {"id": 53, "name": "Citrine Hydro Tumble Stone",    "cat": "Tumbled Stones", "price": 3680, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "citrine hydro tumble stones .jpeg"),         "feat": False},
    {"id": 54, "name": "Aquamarine Tumble Stone",       "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 55, "name": "Carnilane Tumble Stone",        "cat": "Tumbled Stones", "price": 750,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "carnilane tumble stone.jpeg"),               "feat": False},
    {"id": 56, "name": "Dalmatian Tumble Stone",        "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 57, "name": "Sodalite Tumble Stone",         "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "sodalite tumble stone .jpeg"),               "feat": False},
    {"id": 58, "name": "Lapis Lazuli Tumble Stone",     "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "lapiz lazuli tumble stone .jpeg"),           "feat": False},
    {"id": 59, "name": "Hematite Tumble Stone",         "cat": "Tumbled Stones", "price": 750,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 60, "name": "Labradorite Tumble Stone",      "cat": "Tumbled Stones", "price": 750,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 61, "name": "Turquoise Tumble Stone",        "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "torquoise tumble stone .jpeg"),              "feat": False},

    # ══════════════════════════════════════════════════════════════════════════
    # ROUGH STONE (rows 64–70) — Per KG, NO bead size
    # No images available for rough stones
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 64, "name": "Multi Flourite Rough Stone",    "cat": "Rough Stone", "price": 270,  "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},
    {"id": 65, "name": "Carnilane Rough Stone",         "cat": "Rough Stone", "price": 300,  "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},
    {"id": 66, "name": "Black Tourmaline Rough Stone",  "cat": "Rough Stone", "price": 260,  "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},
    {"id": 67, "name": "Green Aventurine Rough Stone",  "cat": "Rough Stone", "price": 300,  "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},
    {"id": 68, "name": "Citrine Natural Rough Stone",   "cat": "Rough Stone", "price": 850,  "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},
    {"id": 69, "name": "Amethyst Rough Stone",          "cat": "Rough Stone", "price": 450,  "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},
    {"id": 70, "name": "Rose Quartz Rough Stone",       "cat": "Rough Stone", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},

    # ══════════════════════════════════════════════════════════════════════════
    # HANGINGS (rows 71–85) — Per PC, no bead
    # No images available for hangings
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 71, "name": "Seven Chakra Tumble with Evil Hanging",          "cat": "HANGINGS", "price": 190,  "p10": 135,  "p50": 120,  "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 72, "name": "Seven Chakra Tumble with Chip Hanging",          "cat": "HANGINGS", "price": 190,  "p10": 140,  "p50": 125,  "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 73, "name": "Pyrite Cluster Evil Eye Hanging",                "cat": "HANGINGS", "price": 190,  "p10": 130,  "p50": 115,  "unit": "per piece", "img": (None, ""), "feat": True},
    {"id": 74, "name": "Metal Pyrite Cluster Hanging",                   "cat": "HANGINGS", "price": 190,  "p10": 140,  "p50": 125,  "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 75, "name": "Clear Quartz Tumble with Evil Eye Hanging",      "cat": "HANGINGS", "price": 230,  "p10": 190,  "p50": 160,  "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 76, "name": "Metal Seven Chakra 21 Beads Hanging",           "cat": "HANGINGS", "price": 160,  "p10": 115,  "p50": 95,   "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 77, "name": "Metal Seven Chakra 15 Beads Hanging",           "cat": "HANGINGS", "price": 150,  "p10": 110,  "p50": 90,   "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 78, "name": "3 Evil Eye with Pyrite Cluster Hanging",         "cat": "HANGINGS", "price": 160,  "p10": 115,  "p50": 95,   "unit": "per piece", "img": (None, ""), "feat": True},
    {"id": 79, "name": "Black Tourmaline & Selenite with Evil Eye Dori", "cat": "HANGINGS", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 80, "name": "Black Tourmaline Hanging",                      "cat": "HANGINGS", "price": 110,  "p10": 85,   "p50": 65,   "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 81, "name": "Selenite Hanging",                              "cat": "HANGINGS", "price": 110,  "p10": 85,   "p50": 65,   "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 82, "name": "Black Tourmaline with Evil Eye Hanging",         "cat": "HANGINGS", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 83, "name": "Selenite with Evil Eye Hanging",                 "cat": "HANGINGS", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 84, "name": "Pyrite Cluster Key Chain 3 PC",                  "cat": "HANGINGS", "price": 110,  "p10": 85,   "p50": 65,   "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 85, "name": "Pyrite Cluster Key Chain 1 PC",                  "cat": "HANGINGS", "price": 110,  "p10": 85,   "p50": 65,   "unit": "per piece", "img": (None, ""), "feat": False},

    # ══════════════════════════════════════════════════════════════════════════
    # ZIBU COINS (rows 86–89) — Per PC, no bead
    # Images in products/zibu_coins/ on ImageKit
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 86, "name": "Green Jade Zibu Coin",     "cat": "Zibu Coin", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": ("zibu", "green jade .jpeg"),              "feat": True},
    {"id": 87, "name": "Pyrite Zibu Coin",         "cat": "Zibu Coin", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": ("zibu", "pyrite zibu coin .jpeg"),        "feat": True},
    {"id": 88, "name": "Rose Quartz Zibu Coin",    "cat": "Zibu Coin", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": ("zibu", "rose quatz coin .jpeg"),         "feat": True},
    {"id": 89, "name": "Seven Chakra Zibu Coin",   "cat": "Zibu Coin", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": ("zibu", "seven chakra zibu coin .jpeg"),  "feat": True},

    # ══════════════════════════════════════════════════════════════════════════
    # BRACELET CHIP (rows 90–95) — Per PC, no bead
    # No images available (except Money Magnet which is in root)
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 90, "name": "7 Chakra Chip Bracelet",    "cat": "BRACELET CHIP", "price": 250, "p10": 195, "p50": 175, "unit": "per piece", "img": (None, "seven chakra (2).png"),  "feat": True},
    {"id": 91, "name": "Dhanyog Chip Bracelet",     "cat": "BRACELET CHIP", "price": 250, "p10": 195, "p50": 175, "unit": "per piece", "img": (None, ""),                      "feat": False},
    {"id": 92, "name": "Money Magnet Chip Bracelet", "cat": "BRACELET CHIP", "price": 250, "p10": 195, "p50": 175, "unit": "per piece", "img": (None, "money magnet.jpg"),      "feat": True},
    {"id": 93, "name": "Carnilane Chip Bracelet",   "cat": "BRACELET CHIP", "price": 250, "p10": 195, "p50": 175, "unit": "per piece", "img": (None, ""),                      "feat": False},
    {"id": 94, "name": "Rose Chip Bracelet",        "cat": "BRACELET CHIP", "price": 250, "p10": 195, "p50": 175, "unit": "per piece", "img": (None, ""),                      "feat": False},
    {"id": 95, "name": "Amethyst Chip Bracelet",    "cat": "BRACELET CHIP", "price": 250, "p10": 195, "p50": 175, "unit": "per piece", "img": (None, ""),                      "feat": False},

    # ══════════════════════════════════════════════════════════════════════════
    # ORGONE PYRAMID (rows 96–100) — Per PC, no bead
    # No images available
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 96,  "name": "Citrine 3 Inch Orgone Pyramid",        "cat": "Orgone Pyramid", "price": 250, "p10": 195, "p50": 170, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 97,  "name": "Laxmi Shree Yantra 4 Inch Pyramid",    "cat": "Orgone Pyramid", "price": 290, "p10": 220, "p50": 190, "unit": "per piece", "img": (None, ""), "feat": True},
    {"id": 98,  "name": "Pyrite Laxmi Pyramid",                 "cat": "Orgone Pyramid", "price": 250, "p10": 195, "p50": 170, "unit": "per piece", "img": (None, ""), "feat": True},
    {"id": 99,  "name": "Money Magnet Orgone Pyramid",          "cat": "Orgone Pyramid", "price": 250, "p10": 195, "p50": 170, "unit": "per piece", "img": (None, ""), "feat": True},
    {"id": 100, "name": "Black Tourmaline Orgone Pyramid",      "cat": "Orgone Pyramid", "price": 250, "p10": 195, "p50": 170, "unit": "per piece", "img": (None, ""), "feat": False},

    # ══════════════════════════════════════════════════════════════════════════
    # SELENITE STONE (rows 101–109) — Per PC, no bead
    # Images in products/selenite_charging_plates_and_lamp/ on ImageKit
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 101, "name": "Selenite Round Shape Plate Plain",    "cat": "Selenite Stone", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": ("selenite", "PLAIN ROUND SHAPE SELENITE PLATE.jpeg"),          "feat": False},
    {"id": 102, "name": "Selenite Round Shape Plate Carving",  "cat": "Selenite Stone", "price": 220,  "p10": 150,  "p50": 110,  "unit": "per piece", "img": ("selenite", "round shape carving selenite plate .jpeg"),       "feat": True},
    {"id": 103, "name": "Selenite Round Bowl",                 "cat": "Selenite Stone", "price": 450,  "p10": 380,  "p50": 345,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},
    {"id": 104, "name": "Selenite Star Moon Bowl",             "cat": "Selenite Stone", "price": 460,  "p10": 390,  "p50": 355,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},
    {"id": 105, "name": "Selenite Any Shape Bowl 3 Inch",      "cat": "Selenite Stone", "price": 460,  "p10": 390,  "p50": 355,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},
    {"id": 106, "name": "Selenite Lamp (Owl)",                 "cat": "Selenite Stone", "price": 220,  "p10": 170,  "p50": 150,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},
    {"id": 107, "name": "Selenite Lamp (Square)",              "cat": "Selenite Stone", "price": 220,  "p10": 170,  "p50": 150,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},
    {"id": 108, "name": "Seven Chakra Selenite Lamp",          "cat": "Selenite Stone", "price": 280,  "p10": 220,  "p50": 180,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},
    {"id": 109, "name": "Citrine Selenite Lamp",               "cat": "Selenite Stone", "price": 300,  "p10": 250,  "p50": 205,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},

    # ══════════════════════════════════════════════════════════════════════════
    # TORTOISE (rows 110–112) — Per PC, no bead
    # No images available
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 110, "name": "Money Magnet Tortoise",   "cat": "TORTOISE", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 111, "name": "Pyrite Tortoise",         "cat": "TORTOISE", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 112, "name": "Angels 2 Inch Tortoise",  "cat": "TORTOISE", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},

    # ══════════════════════════════════════════════════════════════════════════
    # GEMSTONE PENDANT (rows 113–121, unique only — 122–128 are duplicates)
    # Per PC, no bead — No images available
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 113, "name": "Rose Quartz Pendant",           "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 114, "name": "Amethyst Pendant",              "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 115, "name": "Green Aventurine Pendant",      "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 116, "name": "Clear Quartz Pendant",          "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 117, "name": "Tiger Eye Pendant",             "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 118, "name": "Red Jasper Pendant",            "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 119, "name": "Opal Pendant",                  "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 120, "name": "Lapis Lazuli Pendant",          "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 121, "name": "Pencil Cap Pendant Single Point", "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},

    # ══════════════════════════════════════════════════════════════════════════
    # RING (rows 129–133) — Per PC, no bead — No images available
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 129, "name": "Citrine Ring",         "cat": "RING", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 130, "name": "Amethyst Ring",        "cat": "RING", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 131, "name": "Pyrite Ring",          "cat": "RING", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 132, "name": "Black Obsidian Ring",  "cat": "RING", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 133, "name": "Tiger Eye Ring",       "cat": "RING", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},

    # ══════════════════════════════════════════════════════════════════════════
    # CHIPS (rows 134–148) — Per KG, NO bead size
    # Images in products/chips/ on ImageKit
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 134, "name": "Amethyst Chips",          "cat": "CHIPS", "price": 170,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "amethyst chips 1.jpeg"),          "feat": True},
    {"id": 135, "name": "Clear Quartz Chips",      "cat": "CHIPS", "price": 170,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "clear quatz chips .jpeg"),        "feat": False},
    {"id": 136, "name": "Rose Quartz Chips",       "cat": "CHIPS", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("chips", ""),                                "feat": False},
    {"id": 137, "name": "Garnet Chips",            "cat": "CHIPS", "price": 210,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "garnate chips .jpeg"),             "feat": False},
    {"id": 138, "name": "Rainbow Moonstone Chips", "cat": "CHIPS", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "rainbow moonstone chips .jpeg"),  "feat": True},
    {"id": 139, "name": "Amazonite Chips",         "cat": "CHIPS", "price": 180,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "amazonite chips .jpeg"),           "feat": False},
    {"id": 140, "name": "Green Jade Chips",        "cat": "CHIPS", "price": 180,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "green jade chips .jpeg"),          "feat": False},
    {"id": 141, "name": "Green Aventurine Chips",  "cat": "CHIPS", "price": 180,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "green aventurine chips .jpeg"),    "feat": False},
    {"id": 142, "name": "Sunstone Chips",          "cat": "CHIPS", "price": 180,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", ""),                                "feat": False},
    {"id": 143, "name": "Black Agate Chips",       "cat": "CHIPS", "price": 180,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "black agate chips .jpeg"),         "feat": False},
    {"id": 144, "name": "Carnilane Chips",         "cat": "CHIPS", "price": 170,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "carnilane chips .jpeg"),            "feat": False},
    {"id": 145, "name": "White Agate Chips",       "cat": "CHIPS", "price": 160,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "white agate chips .jpeg"),          "feat": False},
    {"id": 146, "name": "Red Jasper Chips",        "cat": "CHIPS", "price": 170,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", ""),                                "feat": False},
    {"id": 147, "name": "Yellow Aventurine Chips",  "cat": "CHIPS", "price": 180,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "yellow aventurine chip.jpeg"),    "feat": False},
    {"id": 148, "name": "Lapis Lazuli Chips",      "cat": "CHIPS", "price": 410,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "lapiz lazuli chips .jpeg"),         "feat": True},
]


class Command(BaseCommand):
    help = "Seed database with exact product data from spreadsheet, with correct categories, prices, and ImageKit image URLs."

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
            coll, cat = TAXONOMY.get(item["cat"], ("BEST SELLERS", item["cat"]))

            slug = slugify(item["name"])
            base, n = slug, 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1

            # Extract stone type from product name by removing category suffixes
            stone_type = item["name"]
            for suffix in [" Bracelet", " Anklet", " Tree", " Tumble Stone", " Rough Stone",
                           " Zibu Coin", " Chip Bracelet", " Chips", " Pyramid",
                           " Orgone Pyramid", " Pendant", " Ring", " Hanging",
                           " Tortoise", " Dori", " Single Point"]:
                stone_type = stone_type.replace(suffix, "")
            stone_type = stone_type.strip()

            # Build image URL from (folder_key, filename) tuple
            folder_key, filename = item["img"]
            if filename:
                img_url = ik_url(folder_key, filename)
            else:
                img_url = f"https://placehold.co/480x480/f5f0e8/c9a84c?text={quote(item['name'])}"

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
                bead_size=item.get("bead", ""),   # Only bracelets have bead size
                size_info=item.get("size_info", ""),
                gender="Unisex",
                collection=coll,
                category=cat,
                image_url=img_url,
                whatsapp_link=wa_link,
                is_featured=item.get("feat", False),
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {created} products with exact spreadsheet data!"))
