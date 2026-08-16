import os
from urllib.parse import quote
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Product, WristSize

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

IK_BASE = "https://ik.imagekit.io/stoneaura/products/"

IK_FOLDERS = {
    "anklet":    "anklet",
    "bead_lines": "bead_lines",
    "chips":     "chips",
    "selenite":  "selenite_charging_plates_and_lamp",
    "tree":      "tree_photos",
    "tumble":    "tumble_stones",
    "zibu":      "zibu_coins",
}

import re

def clean_filename(name):
    # ImageKit replaces each special character/space with a single underscore, preserving consecutive underscores.
    return re.sub(r'[^a-zA-Z0-9.\-_]', '_', name)

def ik_url(folder_key, filename):
    if not filename:
        return ""
    cleaned_name = clean_filename(filename)
    # URL encode only valid special characters if necessary (like quotes/special characters)
    cleaned_name_escaped = quote(cleaned_name)
    if folder_key:
        folder = IK_FOLDERS[folder_key]
        return f"{IK_BASE}{folder}/{cleaned_name_escaped}"
    return f"{IK_BASE}{cleaned_name_escaped}"

PRODUCTS_DATA = [
    # Gemstone Bracelets (1-32)
    {"id": 1,  "name": "Amethyst Bracelet",           "cat": "Gemstone Bracelets", "price": 280,  "p10": 230,  "p50": 180,  "unit": "per piece", "img": (None, "AMETHYST.jpg"),                                "bead": "8mm", "feat": True},
    {"id": 2,  "name": "Carnilane Bracelet",          "cat": "Gemstone Bracelets", "price": 200,  "p10": 150,  "p50": 120,  "unit": "per piece", "img": (None, "carnelian92.webp"),                            "bead": "8mm", "feat": True},
    {"id": 3,  "name": "Green Aventurine Bracelet",   "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "GREEN_AVENTURINE_37360b00-daef-412f-a484-51ebfba2092e.webp"), "bead": "8mm", "feat": True},
    {"id": 4,  "name": "Green Jade Bracelet",         "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "Green-Jade-Bracelet-Final-1.webp"),            "bead": "8mm", "feat": True},
    {"id": 5,  "name": "Appetite Bracelet",           "cat": "Gemstone Bracelets", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},
    {"id": 6,  "name": "Lapiz Bracelet",              "cat": "Gemstone Bracelets", "price": 390,  "p10": 320,  "p50": 250,  "unit": "per piece", "img": (None, "lapiz.webp"),                                 "bead": "8mm", "feat": True},
    {"id": 7,  "name": "Sodalite Bracelet",           "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "sodalite-gemstones-bracelet-1.jpg"),           "bead": "8mm", "feat": False},
    {"id": 8,  "name": "Rose Quartz Bracelet",        "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "ROSE QUATZ IM 1.jpg"),                        "bead": "8mm", "feat": True},
    {"id": 9,  "name": "Calcite Bracelet",            "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "CALCITE.webp"),                               "bead": "8mm", "feat": False},
    {"id": 10, "name": "Sunstone Dyed Bracelet",      "cat": "Gemstone Bracelets", "price": 270,  "p10": 150,  "p50": 130,  "unit": "per piece", "img": (None, "sunstone.jpg"),                               "bead": "8mm", "feat": False},
    {"id": 11, "name": "Sunstone Bracelet",           "cat": "Gemstone Bracelets", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, "sunstone.jpg"),                               "bead": "8mm", "feat": False},
    {"id": 12, "name": "Torquoise Bracelet",          "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "TOURQOUIS.webp"),                             "bead": "8mm", "feat": True},
    {"id": 13, "name": "Black Obsedian Bracelet",     "cat": "Gemstone Bracelets", "price": 180,  "p10": 145,  "p50": 115,  "unit": "per piece", "img": (None, "BLACK OBSEDIAN.webp"),                        "bead": "8mm", "feat": True},
    {"id": 14, "name": "Black Obsedian 8 mm",         "cat": "Gemstone Bracelets", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, "BLACK OBSEDIAN.webp"),                        "bead": "8mm", "feat": False},
    {"id": 15, "name": "Black Tourmuline Bracelet",   "cat": "Gemstone Bracelets", "price": 280,  "p10": 230,  "p50": 180,  "unit": "per piece", "img": (None, "BLACK TOURMALINE.webp"),                      "bead": "8mm", "feat": True},
    {"id": 16, "name": "Tiger Eye Bracelet",          "cat": "Gemstone Bracelets", "price": 180,  "p10": 145,  "p50": 115,  "unit": "per piece", "img": (None, "TIGER_EYE.webp"),                             "bead": "8mm", "feat": True},
    {"id": 17, "name": "Citrine Hydro Bracelet",      "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "CITRINE HYDRO.webp"),                         "bead": "8mm", "feat": False},
    {"id": 18, "name": "Citrine Bracelet",            "cat": "Gemstone Bracelets", "price": 380,  "p10": 290,  "p50": 250,  "unit": "per piece", "img": (None, "CITRINE.jpg"),                                "bead": "8mm", "feat": True},
    {"id": 19, "name": "LAVA Bracelet",               "cat": "Gemstone Bracelets", "price": 150,  "p10": 110,  "p50": 85,   "unit": "per piece", "img": (None, "lava bracelet.webp"),                         "bead": "8mm", "feat": False},
    {"id": 20, "name": "Amazonite Bracelet",          "cat": "Gemstone Bracelets", "price": 250,  "p10": 195,  "p50": 150,  "unit": "per piece", "img": (None, "AMAZONITE.webp"),                             "bead": "8mm", "feat": True},
    {"id": 21, "name": "Sulemani Akik Bracelet",      "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},
    {"id": 22, "name": "Rhodonite Bracelet",          "cat": "Gemstone Bracelets", "price": 200,  "p10": 170,  "p50": 150,  "unit": "per piece", "img": (None, "RHODONITE_001fd9ac-08a2-4d42-9b10-30a73fbc9134.webp"), "bead": "8mm", "feat": False},
    {"id": 23, "name": "Rhodocrosite Bracelet",       "cat": "Gemstone Bracelets", "price": 230,  "p10": 180,  "p50": 160,  "unit": "per piece", "img": (None, "RHODOCROSITE_00ac6fb4-328e-467b-aa89-ec1a5213876b.webp"), "bead": "8mm", "feat": False},
    {"id": 24, "name": "Hematite Bracelet",           "cat": "Gemstone Bracelets", "price": 150,  "p10": 110,  "p50": 90,   "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},
    {"id": 25, "name": "Golden Pyrite Bracelet",      "cat": "Gemstone Bracelets", "price": 150,  "p10": 110,  "p50": 90,   "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},
    {"id": 26, "name": "Natural Pyrite Bracelet",     "cat": "Gemstone Bracelets", "price": 280,  "p10": 240,  "p50": 195,  "unit": "per piece", "img": (None, "NATURAL_PYRITE.webp"),                        "bead": "8mm", "feat": True},
    {"id": 27, "name": "Moonstone Bracelet",          "cat": "Gemstone Bracelets", "price": 390,  "p10": 320,  "p50": 250,  "unit": "per piece", "img": (None, "moon stone.jpg"),                             "bead": "8mm", "feat": True},
    {"id": 28, "name": "Clear Quatz Bracelet",        "cat": "Gemstone Bracelets", "price": 290,  "p10": 240,  "p50": 190,  "unit": "per piece", "img": (None, "CLEAR QUATZ.webp"),                           "bead": "8mm", "feat": False},
    {"id": 29, "name": "Red Jasper Bracelet",         "cat": "Gemstone Bracelets", "price": 190,  "p10": 140,  "p50": 110,  "unit": "per piece", "img": (None, "RED JASPER_.jpg"),                            "bead": "8mm", "feat": True},
    {"id": 30, "name": "Yellow Cat-Eye Bracelet",     "cat": "Gemstone Bracelets", "price": 290,  "p10": 240,  "p50": 190,  "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},
    {"id": 31, "name": "Black Cat Eye Bracelet",      "cat": "Gemstone Bracelets", "price": 460,  "p10": 420,  "p50": 390,  "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},
    {"id": 32, "name": "Karungilini Mala",            "cat": "Gemstone Bracelets", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""),                                           "bead": "8mm", "feat": False},

    # Gemstone Tree (33-36)
    {"id": 33, "name": "Seven Charka Tree",   "cat": "Gemstone Tree", "price": 350,  "p10": 295,  "p50": 255,  "unit": "per piece", "img": ("tree", "seven chakra tree 300 chips.jpg"),   "feat": True},
    {"id": 34, "name": "Money Magnet Tree",   "cat": "Gemstone Tree", "price": 320,  "p10": 290,  "p50": 275,  "unit": "per piece", "img": ("tree", "money magnet tree 300 chips.png"),   "feat": True},
    {"id": 35, "name": "Rose Quatz Tree",     "cat": "Gemstone Tree", "price": 360,  "p10": 295,  "p50": 250,  "unit": "per piece", "img": ("tree", "rose quatz tree 300 chips.jpg"),     "feat": True},
    {"id": 36, "name": "Evil Eye Tree",       "cat": "Gemstone Tree", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": ("tree", "Pyrite cluster tree.jpg"),            "feat": False},

    # ANKLET (37-39)
    {"id": 37, "name": "DHANYOG Anklet",            "cat": "ANKLET", "price": 180, "p10": 220, "p50": None, "unit": "single/pair", "img": ("anklet", "money magnet anklet .jpeg"),          "feat": True,  "size_info": "180 Single / 220 Pair"},
    {"id": 38, "name": "PYRITE Anklet",             "cat": "ANKLET", "price": 180, "p10": 220, "p50": None, "unit": "single/pair", "img": ("anklet", "pyrite anklet .jpeg"),                "feat": True,  "size_info": "180 Single / 220 Pair"},
    {"id": 39, "name": "TRIPLE PROTECTION Anklet",  "cat": "ANKLET", "price": 180, "p10": 220, "p50": None, "unit": "single/pair", "img": ("anklet", "triple protection anklet .jpeg"),    "feat": True,  "size_info": "180 Single / 220 Pair"},

    # Tumbled Stones (40-63)
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
    {"id": 51, "name": "Multi flourite Tumble Stone",   "cat": "Tumbled Stones", "price": 1480, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 52, "name": "Citrine Natural Tumble Stone",  "cat": "Tumbled Stones", "price": 1990, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "citrine natural tumble stone .jpeg"),        "feat": True},
    {"id": 53, "name": "Citrine Hydro Tumble Stone",    "cat": "Tumbled Stones", "price": 3680, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "citrine hydro tumble stones .jpeg"),         "feat": False},
    {"id": 54, "name": "Aquamarine Tumble Stone",       "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 55, "name": "Carnilane Tumble Stone",        "cat": "Tumbled Stones", "price": 750,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "carnilane tumble stone.jpeg"),               "feat": False},
    {"id": 56, "name": "Dalmatian Tumble Stone",        "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 57, "name": "Sodalite Tumble Stone",         "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "sodalite tumble stone .jpeg"),               "feat": False},
    {"id": 58, "name": "Lapis lazuli Tumble Stone (1)", "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "lapiz lazuli tumble stone .jpeg"),           "feat": False},
    {"id": 59, "name": "HEMATITE Tumble Stone (1)",     "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 60, "name": "LABRADORITE Tumble Stone (1)",  "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 61, "name": "Lapis lazuli Tumble Stone (2)", "cat": "Tumbled Stones", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", "lapiz lazuli tumble stone .jpeg"),           "feat": False},
    {"id": 62, "name": "HEMATITE Tumble Stone (2)",     "cat": "Tumbled Stones", "price": 750,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},
    {"id": 63, "name": "LABRADORITE Tumble Stone (2)",  "cat": "Tumbled Stones", "price": 750,  "p10": None, "p50": None, "unit": "per kg", "img": ("tumble", ""),                                          "feat": False},

    # Rough Stone (64-70)
    {"id": 64, "name": "Multi flourite Rough Stone",    "cat": "Rough Stone", "price": 270,  "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},
    {"id": 65, "name": "Carnilane Rough Stone",         "cat": "Rough Stone", "price": 300,  "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},
    {"id": 66, "name": "Black Tourmaline Rough Stone",  "cat": "Rough Stone", "price": 260,  "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},
    {"id": 67, "name": "Green Aventurine Rough Stone",  "cat": "Rough Stone", "price": 300,  "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},
    {"id": 68, "name": "Citrine Natural Rough Stone",   "cat": "Rough Stone", "price": 850,  "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},
    {"id": 69, "name": "Amethyst Rough Stone",          "cat": "Rough Stone", "price": 450,  "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},
    {"id": 70, "name": "ROSE Rough Stone",              "cat": "Rough Stone", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": (None, ""), "feat": False},

    # HANGINGS (71-85)
    {"id": 71, "name": "SEVEN CHAKRA TUMBLE WITH EVIL HANGING",          "cat": "HANGINGS", "price": 190,  "p10": 135,  "p50": 120,  "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 72, "name": "SEVEN CHAKRA TUMBLE WITH CHIP HANGING",          "cat": "HANGINGS", "price": 190,  "p10": 140,  "p50": 125,  "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 73, "name": "PYRITE CLUSTER EVIL EYE",                        "cat": "HANGINGS", "price": 190,  "p10": 130,  "p50": 115,  "unit": "per piece", "img": (None, ""), "feat": True},
    {"id": 74, "name": "METAL PYRITE CLUSTER HANGING",                   "cat": "HANGINGS", "price": 190,  "p10": 140,  "p50": 125,  "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 75, "name": "CLEAR QUATZ TUMBLE WITH EVIL EYE HANGIING",      "cat": "HANGINGS", "price": 230,  "p10": 190,  "p50": 160,  "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 76, "name": "METAL SEVEN CHAKRA 21 BEADS",                    "cat": "HANGINGS", "price": 160,  "p10": 115,  "p50": 95,   "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 77, "name": "METAL SEVEN CHAKRA 15 BEADS",                    "cat": "HANGINGS", "price": 150,  "p10": 110,  "p50": 90,   "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 78, "name": "3 EVIL EYE WITH PYRITE CLUSTER",                 "cat": "HANGINGS", "price": 160,  "p10": 115,  "p50": 95,   "unit": "per piece", "img": (None, ""), "feat": True},
    {"id": 79, "name": "BLACK TOURMULINE & SELENITE WITH EVIL EYE",      "cat": "HANGINGS", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 80, "name": "BLACK TOURMULINE Hanging",                       "cat": "HANGINGS", "price": 110,  "p10": 85,   "p50": 65,   "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 81, "name": "SELENITE Hanging",                               "cat": "HANGINGS", "price": 110,  "p10": 85,   "p50": 65,   "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 82, "name": "BLACK TOURMULINE WITH EVIL EYE",                 "cat": "HANGINGS", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 83, "name": "SELENITE WITH EVIL EYE",                         "cat": "HANGINGS", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 84, "name": "PYRITE CLUSTER KEY CHAIN 3 PC",                  "cat": "HANGINGS", "price": 110,  "p10": 85,   "p50": 65,   "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 85, "name": "PYRITE CLUSTER KEY CHAIN 1PC",                   "cat": "HANGINGS", "price": 110,  "p10": 85,   "p50": 65,   "unit": "per piece", "img": (None, ""), "feat": False},

    # Zibu Coin (86-89)
    {"id": 86, "name": "GREEN JADE Zibu Coin",     "cat": "Zibu Coin", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": ("zibu", "green jade .jpeg"),              "feat": True},
    {"id": 87, "name": "PYRITE Zibu Coin",         "cat": "Zibu Coin", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": ("zibu", "pyrite zibu coin .jpeg"),        "feat": True},
    {"id": 88, "name": "ROSE Zibu Coin",           "cat": "Zibu Coin", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": ("zibu", "rose quatz coin .jpeg"),         "feat": True},
    {"id": 89, "name": "SEVEN CHAKRA Zibu Coin",   "cat": "Zibu Coin", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": ("zibu", "seven chakra zibu coin .jpeg"),  "feat": True},

    # BRACELET CHIP (90-95)
    {"id": 90, "name": "7 CHAKRA Chip Bracelet",    "cat": "BRACELET CHIP", "price": 250, "p10": 195, "p50": 175, "unit": "per piece", "img": (None, "seven chakra (2).png"),  "feat": True},
    {"id": 91, "name": "DHANYOG Chip Bracelet",     "cat": "BRACELET CHIP", "price": 250, "p10": 195, "p50": 175, "unit": "per piece", "img": (None, ""),                      "feat": False},
    {"id": 92, "name": "MONEY MAGNET Chip Bracelet", "cat": "BRACELET CHIP", "price": 250, "p10": 195, "p50": 175, "unit": "per piece", "img": (None, "money magnet.jpg"),      "feat": True},
    {"id": 93, "name": "CARNILANE Chip Bracelet",   "cat": "BRACELET CHIP", "price": 250, "p10": 195, "p50": 175, "unit": "per piece", "img": (None, ""),                      "feat": False},
    {"id": 94, "name": "ROSE Chip Bracelet",        "cat": "BRACELET CHIP", "price": 250, "p10": 195, "p50": 175, "unit": "per piece", "img": (None, ""),                      "feat": False},
    {"id": 95, "name": "AMETHYST Chip Bracelet",    "cat": "BRACELET CHIP", "price": 250, "p10": 195, "p50": 175, "unit": "per piece", "img": (None, ""),                      "feat": False},

    # Orgone Pyramid (96-100)
    {"id": 96,  "name": "CITRINE 3 INCH Orgone Pyramid",        "cat": "Orgone Pyramid", "price": 250, "p10": 195, "p50": 170, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 97,  "name": "LAXMI SHREE YANTRA 4 INCH Pyramid",    "cat": "Orgone Pyramid", "price": 290, "p10": 220, "p50": 190, "unit": "per piece", "img": (None, ""), "feat": True},
    {"id": 98,  "name": "PYRITE LAXMI PYRAMID",                 "cat": "Orgone Pyramid", "price": 250, "p10": 195, "p50": 170, "unit": "per piece", "img": (None, ""), "feat": True},
    {"id": 99,  "name": "MONEY MAGNET Orgone Pyramid",          "cat": "Orgone Pyramid", "price": 250, "p10": 195, "p50": 170, "unit": "per piece", "img": (None, ""), "feat": True},
    {"id": 100, "name": "BLACK TORMULINE Orgone Pyramid",      "cat": "Orgone Pyramid", "price": 250, "p10": 195, "p50": 170, "unit": "per piece", "img": (None, ""), "feat": False},

    # Selenite Stone (101-109)
    {"id": 101, "name": "SELENITE ROUND SHAPE PLATE PAIN",    "cat": "Selenite Stone", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": ("selenite", "PLAIN ROUND SHAPE SELENITE PLATE.jpeg"),          "feat": False},
    {"id": 102, "name": "SELENITE ROUND SHAPE PLATE CARVING",  "cat": "Selenite Stone", "price": 220,  "p10": 150,  "p50": 110,  "unit": "per piece", "img": ("selenite", "round shape carving selenite plate .jpeg"),       "feat": True},
    {"id": 103, "name": "ROUND BOWL",                          "cat": "Selenite Stone", "price": 450,  "p10": 380,  "p50": 345,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},
    {"id": 104, "name": "STAR MOON Selenite Bowl",             "cat": "Selenite Stone", "price": 460,  "p10": 390,  "p50": 355,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},
    {"id": 105, "name": "ANY SHAPE IN BOWL IN 3 INCH",          "cat": "Selenite Stone", "price": 460,  "p10": 390,  "p50": 355,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},
    {"id": 106, "name": "SELENITE LAMP (OWL)",                 "cat": "Selenite Stone", "price": 220,  "p10": 170,  "p50": 150,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},
    {"id": 107, "name": "SELENITE LAMP (SQAURE )",              "cat": "Selenite Stone", "price": 220,  "p10": 170,  "p50": 150,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},
    {"id": 108, "name": "SEVEN CHAKRA LAMP",                  "cat": "Selenite Stone", "price": 280,  "p10": 220,  "p50": 180,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},
    {"id": 109, "name": "CITRINE LAMP",                       "cat": "Selenite Stone", "price": 300,  "p10": 250,  "p50": 205,  "unit": "per piece", "img": ("selenite", ""),                                                "feat": False},

    # TORTOISE (110-112)
    {"id": 110, "name": "MONEY MAGNET Tortoise",   "cat": "TORTOISE", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 111, "name": "PYRITE Tortoise",         "cat": "TORTOISE", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 112, "name": "ANGLES 2 INCH Tortoise",  "cat": "TORTOISE", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},

    # Gemstone Pendant (113-128)
    {"id": 113, "name": "ROSE QUATZ Pendant (1)",        "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 114, "name": "AMETHYST Pendant (1)",          "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 115, "name": "GREEN AVENTURINE Pendant (1)",  "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 116, "name": "CLEAR QUATZ Pendant (1)",       "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 117, "name": "TIGER EYE Pendant (1)",         "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 118, "name": "RED JASPER Pendant (1)",        "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 119, "name": "OPAL Pendant (1)",              "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 120, "name": "LAPIZ Pendant",                 "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 121, "name": "PENCIL CAP PEDANT SINGLE POINT", "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 122, "name": "ROSE QUATZ Pendant (2)",        "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 123, "name": "AMETHYST Pendant (2)",          "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 124, "name": "GREEN AVENTURINE Pendant (2)",  "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 125, "name": "CLEAR QUATZ Pendant (2)",       "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 126, "name": "TIGER EYE Pendant (2)",         "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 127, "name": "RED JASPER Pendant (2)",        "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 128, "name": "OPAL Pendant (2)",              "cat": "Gemstone Pendant", "price": 130, "p10": 95, "p50": 70, "unit": "per piece", "img": (None, ""), "feat": False},

    # RING (129-133)
    {"id": 129, "name": "CITRINE Ring",         "cat": "RING", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 130, "name": "AMETHYST Ring",        "cat": "RING", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 131, "name": "PYRITE Ring",          "cat": "RING", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 132, "name": "BLACK OBSEDIAN Ring",  "cat": "RING", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},
    {"id": 133, "name": "TIGER EYE Ring",       "cat": "RING", "price": None, "p10": None, "p50": None, "unit": "per piece", "img": (None, ""), "feat": False},

    # CHIPS (134-148)
    {"id": 134, "name": "AMETHYST Chips",          "cat": "CHIPS", "price": 170,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "amethyst chips 1.jpeg"),          "feat": True},
    {"id": 135, "name": "CLEAR QUATZ Chips",      "cat": "CHIPS", "price": 170,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "clear quatz chips .jpeg"),        "feat": False},
    {"id": 136, "name": "ROSE QUATZ Chips",       "cat": "CHIPS", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("chips", ""),                                "feat": False},
    {"id": 137, "name": "GARNET Chips",            "cat": "CHIPS", "price": 210,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "garnate chips .jpeg"),             "feat": False},
    {"id": 138, "name": "RAINBOW MOONSTONE Chips", "cat": "CHIPS", "price": None, "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "rainbow moonstone chips .jpeg"),  "feat": True},
    {"id": 139, "name": "AMAZONITE Chips",         "cat": "CHIPS", "price": 180,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "amazonite chips .jpeg"),           "feat": False},
    {"id": 140, "name": "GREEN JADE Chips",        "cat": "CHIPS", "price": 180,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "green jade chips .jpeg"),          "feat": False},
    {"id": 141, "name": "GREEN AVENTURIN E Chips",  "cat": "CHIPS", "price": 180,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "green aventurine chips .jpeg"),    "feat": False},
    {"id": 142, "name": "SUNSTONE Chips",          "cat": "CHIPS", "price": 180,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", ""),                                "feat": False},
    {"id": 143, "name": "BLACK AGATE Chips",       "cat": "CHIPS", "price": 180,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "black agate chips .jpeg"),         "feat": False},
    {"id": 144, "name": "CARNILANE Chips",         "cat": "CHIPS", "price": 170,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "carnilane chips .jpeg"),            "feat": False},
    {"id": 145, "name": "WHITE AGATE Chips",       "cat": "CHIPS", "price": 160,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "white agate chips .jpeg"),          "feat": False},
    {"id": 146, "name": "RED JASPER Chips",        "cat": "CHIPS", "price": 170,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", ""),                                "feat": False},
    {"id": 147, "name": "YELLO AVENTURINE Chips",  "cat": "CHIPS", "price": 180,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "yellow aventurine chip.jpeg"),    "feat": False},
    {"id": 148, "name": "LAPIZ Chips",             "cat": "CHIPS", "price": 410,  "p10": None, "p50": None, "unit": "per kg", "img": ("chips", "lapiz lazuli chips .jpeg"),         "feat": True},
]


class Command(BaseCommand):
    help = "Seed database with exactly 148 product data from spreadsheet, with correct categories, prices, and ImageKit image URLs."

    def handle(self, *args, **options):
        Product.objects.all().delete()
        self.stdout.write(self.style.WARNING("Cleared all products from the database."))

        WristSize.objects.all().delete()
        WristSize.objects.bulk_create([WristSize(**ws) for ws in WRIST_SIZES])
        self.stdout.write(self.style.SUCCESS(f"  [OK]  {len(WRIST_SIZES)} wrist sizes seeded."))

        created = 0
        for item in PRODUCTS_DATA:
            coll, cat = TAXONOMY.get(item["cat"], ("BEST SELLERS", item["cat"]))

            # Generate unique slug for every product, including duplicates
            slug = slugify(item["name"])
            base, n = slug, 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1

            stone_type = item["name"]
            # Clean up suffix and markers
            for marker in [" (1)", " (2)", " (OWL)", " (SQAURE )", " (OWL)", " (Square)"]:
                stone_type = stone_type.replace(marker, "")
            for suffix in [" Bracelet", " Anklet", " Tree", " Tumble Stone", " Rough Stone",
                           " Zibu Coin", " Chip Bracelet", " Chips", " Pyramid",
                           " Orgone Pyramid", " Pendant", " Ring", " Hanging",
                           " Tortoise", " Dori", " Single Point"]:
                stone_type = stone_type.replace(suffix, "")
            stone_type = stone_type.strip().title()

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
