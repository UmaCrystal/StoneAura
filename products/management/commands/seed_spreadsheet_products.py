import os
import re
import csv
from pathlib import Path
from urllib.parse import quote
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Product, WristSize

class Command(BaseCommand):
    help = "Seed database with products from the spreadsheet, using mapping_report.md for image URLs."

    def handle(self, *args, **options):
        # 1. Clean up existing products
        Product.objects.all().delete()
        self.stdout.write(self.style.WARNING("Cleared all products from the database."))

        # 2. Parse mapping_report.md to get the final image mappings
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        report_path = base_dir / "mapping_report.md"
        csv_path = Path(r"C:\Users\baps\.gemini\antigravity-ide\brain\bd07581c-f9a8-4b1f-bce2-5a586ca969d5\.system_generated\steps\19\content.md")

        if not report_path.exists():
            self.stdout.write(self.style.ERROR(f"Error: {report_path} not found! Run mapping generator first."))
            return

        # Map: product_id (int) -> renamed_image_path (str)
        image_mappings = {}
        
        with open(report_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            if line.strip().startswith("|") and not line.strip().startswith("| ---"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 7 and parts[1].isdigit():
                    prod_id = int(parts[1])
                    new_img_raw = parts[6].strip()
                    new_img = new_img_raw.replace("`", "") if new_img_raw else ""
                    if new_img and new_img != "*BLANK*":
                        image_mappings[prod_id] = new_img

        # 3. Parse spreadsheet products CSV
        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f"Error: CSV path {csv_path} not found!"))
            return

        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        csv_rows = []
        for line in lines:
            if line.strip().startswith(",") or re.match(r"^\s*,", line):
                reader = csv.reader([line.strip()])
                csv_rows.append(next(reader))

        products_data = []
        current_category = None

        FRONTEND_TAXONOMY = {
            "Gemstone Bracelets": ("BEST SELLERS", "Gemstone Bracelets"),
            "TREE": ("BEST SELLERS", "Gemstone Tree"),
            "ANKLET": ("JEWELRY & ACCESSORIES", "Anklets"),
            "TUMBLE STONE": ("BEST SELLERS", "Tumbled Stones"),
            "ROUGH": ("HOME & DECOR", "Rough Stone"),
            "HANGINGS": ("SPIRITUAL & HEALING", "Unique Products"),
            "ZIBU COINS": ("HOME & DECOR", "Zibu Coin"),
            "BRACELET CHIP": ("JEWELRY & ACCESSORIES", "Tumbled Bracelets"),
            "PYRAMIDS": ("BEST SELLERS", "Pyramid Stone"),
            "SELENITE PRODUCTS": ("BEST SELLERS", "Selenite Stone"),
            "TORTOISE": ("SPIRITUAL & HEALING", "Unique Products"),
            "ANGLES 2 INCH": ("SPIRITUAL & HEALING", "Gemstone Angels"),
            "PEDANTS": ("JEWELRY & ACCESSORIES", "Gemstone Pendant"),
            "RING": ("JEWELRY & ACCESSORIES", "Gemstone"),
            "CHIPS": ("BEST SELLERS", "Healing Crystals")
        }

        for row in csv_rows:
            row = [x.strip() for x in row]
            if not any(row):
                continue

            val2 = row[2] if len(row) > 2 else ""
            val3 = row[3] if len(row) > 3 else ""

            # Check both columns for headers, stripping spaces
            clean_val2 = val2.strip().upper()
            clean_val3 = val3.strip().upper()

            if "NAME OF THE PRODUCTS" in clean_val2 or "NAME OF THE PRODUCTS" in clean_val3:
                current_category = "Gemstone Bracelets"
                continue

            header_cats = ["TREE", "ANKLET", "TUMBLE STONE", "ROUGH", "HANGINGS", "ZIBU COINS", "BRACELET CHIP", "PYRAMIDS", "SELENITE PRODUCTS", "TORTOISE", "ANGLES 2 INCH", "PEDANTS", "RING", "CHIPS"]
            matched_cat = None
            for cat_name in header_cats:
                if cat_name in clean_val2 or cat_name in clean_val3:
                    matched_cat = cat_name
                    break

            if matched_cat:
                current_category = matched_cat
                continue

            if val2.isdigit():
                prod_id = int(val2)
                prod_name = val3

                # Pricing rules
                price = None
                price_10pc = None
                price_50pc = None
                price_unit = "per piece"

                if current_category == "TUMBLE STONE" or current_category == "ROUGH" or current_category == "CHIPS":
                    cost = row[4] if len(row) > 4 else ""
                    per_kg = row[5] if len(row) > 5 else ""
                    price_val = per_kg if per_kg else cost
                    price = float(price_val) if price_val else None
                    price_unit = "per kg" if per_kg else "per piece"
                elif current_category == "ANKLET":
                    price_val = row[4] if len(row) > 4 else ""
                    # For anklet: "180 SINGLE PC /220 PAIR" => let's store 180 as price, and full string as size_info or description?
                    # Or set price=180, price_unit='single/pair'
                    # Let's extract the first number as base price
                    match = re.search(r'\d+', price_val)
                    price = float(match.group(0)) if match else None
                    price_unit = "single/pair"
                else:
                    price_val = row[5] if len(row) > 5 else ""
                    p10_val = row[6] if len(row) > 6 else ""
                    p50_val = row[7] if len(row) > 7 else ""
                    
                    price = float(price_val) if price_val else None
                    price_10pc = float(p10_val) if p10_val else None
                    price_50pc = float(p50_val) if p50_val else None

                # Taxonomy
                coll, cat = FRONTEND_TAXONOMY.get(current_category, ("BEST SELLERS", current_category))

                # Image url from report
                renamed_path = image_mappings.get(prod_id)
                image_url = ""
                if renamed_path:
                    # Clean filename path quotes/spaces
                    filename_escaped = quote(os.path.basename(renamed_path))
                    image_url = f"https://ik.imagekit.io/stoneaura/products/{filename_escaped}"

                products_data.append({
                    "id": prod_id,
                    "name": prod_name,
                    "price": price,
                    "price_10pc": price_10pc,
                    "price_50pc": price_50pc,
                    "price_unit": price_unit,
                    "collection": coll,
                    "category": cat,
                    "image_url": image_url,
                    "size_info": row[4] if current_category == "ANKLET" else "", # save raw anklet price text "180 SINGLE PC /220 PAIR"
                })

        # 4. Create Product objects
        created = 0
        for p in products_data:
            # Slug generation
            slug = slugify(p["name"])
            base, n = slug, 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base}-{n}"
                n += 1

            # Stone type extraction from name
            stone = p["name"].replace(" (N)", "").replace(" (D)", "").replace(" dyed", "").strip()
            # Title Case stone name
            stone = stone.title()

            Product.objects.create(
                id=p["id"],
                name=p["name"].title(),
                slug=slug,
                price=p["price"],
                price_10pc=p["price_10pc"],
                price_50pc=p["price_50pc"],
                price_unit=p["price_unit"],
                stone_type=stone,
                color="",
                material="Natural Gemstone" if "natural" in p["name"].lower() or "(n)" in p["name"].lower() else "Gemstone",
                bead_size="8mm" if p["category"] == "Gemstone Bracelets" else "",
                gender="Unisex",
                collection=p["collection"],
                category=p["category"],
                image_url=p["image_url"],
                size_info=p["size_info"],
                whatsapp_link=f"https://wa.me/919104139899?text=Hi%2C%20I%20am%20interested%20in%20{quote(p['name'])}",
                is_featured=False
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {created} products from spreadsheet!"))
