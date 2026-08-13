from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Product, WristSize

# Precise mapping of filenames under /images/products/
IMG: dict[str, str] = {
    "ROSE_QUARTZ_BRACELET":            "/images/products/ROSE QUATZ IM 1.jpg",
    "PYRITE_NATURAL_STAR_BRACELET":    "/images/products/NATURAL_PYRITE.webp",
    "TURQUOISE_BRACELET":              "/images/products/TOURQOUIS.webp",
    "GREEN_AVENTURINE_BRACELET":       "/images/products/GREEN_AVENTURINE_37360b00-daef-412f-a484-51ebfba2092e.webp",
    "AMETHYST_BRACELET":               "/images/products/AMETHYST.jpg",
    "APATITE_BRACELET":                "/images/products/apatite.png",
    "TIGER_EYE_BRACELET":              "/images/products/TIGER_EYE.webp",
    "LAVA_STONE_BRACELET":             "/images/products/lava bracelet.webp",
    "RED_JASPER_BRACELET":             "/images/products/RED JASPER_.jpg",
    "BLACK_TOURMALINE_BRACELET":       "/images/products/black-tourmaline.png",
    "CITRINE_NATURAL_BRACELET":        "/images/products/CITRINE.webp",
    "CITRINE_HYDRO_BRACELET":          "/images/products/CITRINE 2.jpg",
    "CLEAR_QUARTZ_BRACELET":           "/images/products/clear-quartz.png",
    "MONEY_MAGNET_BRACELET":           "/images/products/money magnet.jpg",
    "SEVEN_CHAKRA_BRACELET":           "/images/products/seven chakra.png",
    "RASHI_BRACELET":                  "/images/products/rashi bracelet.webp",
    "SEVEN_CHAKRA_LAVA_BRACELET":      "/images/products/seven chakra (2).png",
    "DHANYOG_BRACELET":                "/images/products/money magnet.jpg",
    "MOONSTONE_BRACELET":              "/images/products/moon stone.jpg",
    "CARNELIAN_BRACELET":              "/images/products/carnelian92.webp",
    "GREEN_JADE_BRACELET":             "/images/products/Green-Jade-Bracelet-Final-1.webp",
    "LAPIS_LAZULI_BRACELET":           "/images/products/lapiz.webp",
    "SODALITE_BRACELET":               "/images/products/sodalite-gemstones-bracelet-1.jpg",
    "CALCITE_BRACELET":                "/images/products/calcite.jpg",
    "SUNSTONE_BRACELET":               "/images/products/sunstone.jpg",
    "BLACK_OBSIDIAN_BRACELET":         "/images/products/black obsedian.webp",
    "AMAZONITE_BRACELET":              "/images/products/amazomite.webp",
    "RHODONITE_BRACELET":              "/images/products/RHODONITE_001fd9ac-08a2-4d42-9b10-30a73fbc9134.webp",
    "RHODOCHROSITE_BRACELET":          "/images/products/RHODOCROSITE_00ac6fb4-328e-467b-aa89-ec1a5213876b.webp",
    "DHANVRUDDHI_BRACELET":            "/images/products/money magnet.jpg",
}

PLACEHOLDER = "https://placehold.co/480x480/f5f0e8/c9a84c?text={name}"
WA_BASE     = "https://wa.me/919104139899?text=Hi%2C%20I%20am%20interested%20in%20"


def img(key: str, product_name: str) -> str:
    """Return the fully-qualified image URL for a product."""
    original_val = IMG.get(key)
    if original_val:
        if original_val.startswith("/images/products/"):
            from urllib.parse import quote
            filename = original_val.replace("/images/products/", "")
            return f"https://ik.imagekit.io/stoneaura/products/{quote(filename)}"
        return original_val
    return PLACEHOLDER.format(name=product_name.replace(" ", "+"))


def wa(name: str, price: int) -> str:
    return f"{WA_BASE}{name.replace(' ', '%20')}%20priced%20at%20%E2%82%B9{price}"


BRACELETS = [
    # No.  Name                              1pc   10pc  50pc   stone              color                material                    bead   featured
    (  1, "Rose Quartz Bracelet",            280,  250,  190,  "Rose Quartz",     "Baby Pink",         "Natural Rose Quartz",      "8mm",  True),
    (  2, "Pyrite Natural Star Bracelet",    280,  250,  210,  "Pyrite",          "Golden",            "Natural Pyrite",           "8mm",  True),
    (  3, "Turquoise Bracelet",              290,  260,  195,  "Turquoise",       "Sky Blue",          "Natural Turquoise",        "8mm",  True),
    (  4, "Green Aventurine Bracelet",       200,  180,  150,  "Green Aventurine","Forest Green",      "Natural Green Aventurine", "8mm",  True),
    (  5, "Amethyst Bracelet",               300,  280,  250,  "Amethyst",        "Purple",            "Natural Amethyst",         "8mm",  True),
    (  6, "Apatite Bracelet",                380,  350,  310,  "Apatite",         "Blue Green",        "Natural Apatite",          "8mm", False),
    (  7, "Tiger Eye Bracelet",              250,  200,  180,  "Tiger Eye",       "Golden Brown",      "Natural Tiger Eye",        "8mm",  True),
    (  8, "Lava Stone Bracelet",             170,  150,  110,  "Lava Stone",      "Black",             "Natural Volcanic Lava",    "8mm", False),
    (  9, "Red Jasper Bracelet",             250,  230,  190,  "Red Jasper",      "Deep Red",          "Natural Red Jasper",       "8mm",  True),
    ( 10, "Black Tourmaline Bracelet",       280,  250,  180,  "Black Tourmaline","Jet Black",         "Natural Black Tourmaline", "8mm",  True),
    ( 11, "Citrine Natural Bracelet",        380,  350,  300,  "Citrine",         "Golden Yellow",     "Natural Citrine",          "8mm",  True),
    ( 12, "Citrine Hydro Bracelet",          250,  200,  180,  "Citrine",         "Light Yellow",      "Hydro Citrine",            "8mm", False),
    ( 13, "Clear Quartz Bracelet",           280,  250,  210,  "Clear Quartz",    "Crystal Clear",     "Natural Clear Quartz",     "8mm", False),
    ( 14, "Money Magnet Bracelet",           280,  250,  210,  "Mixed Crystals",  "Mixed",             "Natural Stone",            "8mm",  True),
    ( 15, "Seven Chakra Bracelet",           250,  230,  180,  "Seven Chakra",    "Rainbow",           "Mixed Natural Gemstones",  "8mm",  True),
    ( 16, "Rashi Bracelet",                  290,  250,  220,  "Zodiac Crystals", "Mixed",             "Natural Gemstone",         "8mm", False),
    ( 17, "Seven Chakra Lava Bracelet",      200,  260,  210,  "Seven Chakra",    "Rainbow",           "Natural Lava & Crystal",   "8mm", False),
    ( 18, "Dhanyog Bracelet",                280,  250,  210,  "Mixed Crystals",  "Mixed",             "Natural Gemstone",         "8mm", False),
    ( 19, "Moonstone Bracelet",              360,  320,  290,  "Moonstone",       "Pearly White",      "Natural Moonstone",        "8mm",  True),
    ( 20, "Carnelian Bracelet",              290,  250,  210,  "Carnelian",       "Orange Red",        "Natural Carnelian",        "8mm",  True),
    ( 21, "Green Jade Bracelet",             200,  180,  150,  "Green Jade",      "Jade Green",        "Natural Green Jade",       "8mm",  True),
    ( 22, "Lapis Lazuli Bracelet",           400,  360,  300,  "Lapis Lazuli",    "Royal Blue",        "Natural Lapis Lazuli",     "8mm",  True),
    ( 23, "Sodalite Bracelet",               250,  200,  180,  "Sodalite",        "Royal Blue & White","Natural Sodalite",         "8mm", False),
    ( 24, "Calcite Bracelet",                280,  250,  190,  "Calcite",         "White / Orange",    "Natural Calcite",          "8mm", False),
    ( 25, "Sunstone Bracelet",               280,  250,  190,  "Sunstone",        "Orange / Gold",     "Natural Sunstone",         "8mm",  True),
    ( 26, "Black Obsidian Bracelet",         250,  200,  180,  "Black Obsidian",  "Jet Black",         "Natural Black Obsidian",   "8mm",  True),
    ( 27, "Amazonite Bracelet",              250,  230,  180,  "Amazonite",       "Teal Green",        "Natural Amazonite",        "8mm",  True),
    ( 28, "Rhodonite Bracelet",              270,  240,  210,  "Rhodonite",       "Pink & Black",      "Natural Rhodonite",        "8mm", False),
    ( 29, "Rhodochrosite Bracelet",          280,  250,  220,  "Rhodochrosite",   "Pink / Rose",       "Natural Rhodochrosite",    "8mm", False),
    ( 30, "Dhanvruddhi Bracelet",            300,  260,  230,  "Mixed Crystals",  "Mixed",             "Natural Gemstone",         "8mm", False),
]

SELENITE_ITEMS = [
    # No.   Name                               1pc  10pc  50pc  stone       color    material              category
    ( 60, "Seven Chakra Selenite Plate",      180,  150,  130, "Selenite", "White", "Natural Selenite", "Selenite Plates"),
    ( 61, "Rashi Selenite Plate",             230,  190,  160, "Selenite", "White", "Natural Selenite", "Selenite Plates"),
    ( 62, "Pyrite Frame with 7 Horses",         0, None, None, "Pyrite",   "Golden","Natural Pyrite",   "Home Decor"),
    ( 63, "Crystal Keychain",                 180,  150,  120, "Mixed Crystals","Mixed","Natural Gemstone","Keychains"),
]

WRIST_SIZES = [
    {"label": "XS", "cm": "13–14 cm", "inches": '5.1–5.5"'},
    {"label": "S",  "cm": "14–15 cm", "inches": '5.5–5.9"'},
    {"label": "M",  "cm": "15–17 cm", "inches": '5.9–6.7"'},
    {"label": "L",  "cm": "17–18 cm", "inches": '6.7–7.1"'},
    {"label": "XL", "cm": "18–20 cm", "inches": '7.1–7.9"'},
]


class Command(BaseCommand):
    help = "Seed database with exactly the Aurastone wholesale catalogue."

    def handle(self, *args, **options):
        # 1. Clean up ALL existing products to ensure no duplicates or extra ovals
        Product.objects.all().delete()
        self.stdout.write(self.style.WARNING("Cleared all products from the database."))

        # 2. Seed wrist sizes
        self._seed_wrist_sizes()

        # 3. Seed bracelets
        self._seed_bracelets()

        # 4. Seed selenite plates & accessories
        self._seed_other_items()

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))

    # ── private helpers ───────────────────────────────────────────────────

    def _seed_wrist_sizes(self):
        WristSize.objects.all().delete()
        WristSize.objects.bulk_create([WristSize(**ws) for ws in WRIST_SIZES])
        self.stdout.write(self.style.SUCCESS(f"  [OK]  {len(WRIST_SIZES)} wrist sizes"))

    def _seed_bracelets(self):
        created = 0
        for row in BRACELETS:
            num, name, p1, p10, p50, stone, color, material, bead, featured = row
            img_key = name.upper().replace(" ", "_")
            self._create(
                name=name, price=p1, price_10pc=p10, price_50pc=p50,
                stone_type=stone, color=color, material=material,
                bead_size=bead, is_featured=featured,
                img_key=img_key, collection="BEST SELLERS", category="Gemstone Bracelets",
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f"  [OK]  {created} bracelets"))

    def _seed_other_items(self):
        created = 0
        other_mappings = {
            "Seven Chakra Selenite Plate": ("BEST SELLERS", "Selenite Stone"),
            "Rashi Selenite Plate": ("BEST SELLERS", "Selenite Stone"),
            "Pyrite Frame with 7 Horses": ("HOME & DECOR", "Rough Stone"),
            "Crystal Keychain": ("JEWELRY & ACCESSORIES", "Gemstone"),
        }
        for row in SELENITE_ITEMS:
            num, name, p1, p10, p50, stone, color, material, orig_cat = row
            img_key = name.upper().replace(" ", "_")
            coll, cat = other_mappings.get(name, ("BEST SELLERS", orig_cat))
            self._create(
                name=name, price=p1 or 0, price_10pc=p10, price_50pc=p50,
                stone_type=stone, color=color, material=material,
                bead_size="", is_featured=False,
                img_key=img_key, collection=coll, category=cat,
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f"  [OK]  {created} other items"))

    def _create(self, *, name, price, price_10pc, price_50pc,
                stone_type, color, material, bead_size,
                is_featured, img_key, collection, category):
        slug = slugify(name)
        base, n = slug, 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base}-{n}"
            n += 1

        Product.objects.create(
            name=name,
            slug=slug,
            price=price,
            price_10pc=price_10pc,
            price_50pc=price_50pc,
            price_100pc=None,
            stone_type=stone_type,
            color=color,
            material=material,
            bead_size=bead_size,
            gender="Unisex",
            collection=collection,
            category=category,
            is_featured=is_featured,
            image_url=img(img_key, name),
            whatsapp_link=wa(name, price),
        )
