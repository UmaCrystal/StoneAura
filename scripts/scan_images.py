import os
import csv
import re
import sys
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = Path(r"C:\Users\baps\.gemini\antigravity-ide\brain\bd07581c-f9a8-4b1f-bce2-5a586ca969d5\.system_generated\steps\19\content.md")
IMAGES_DIR = BASE_DIR / "frontend" / "public" / "images" / "products"

def clean_name(name):
    """Normalize names for matching."""
    if not name:
        return ""
    # remove (N), (D), (n), (d) etc.
    name = re.sub(r"\s*\([NDnd]\)\s*", "", name)
    name = name.lower().strip()
    name = re.sub(r"[^\w\s\-]", "", name)
    return name

def get_human_size(size_in_bytes):
    """Format bytes as human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"

def main():
    print(f"Base Directory: {BASE_DIR}")
    print(f"CSV Path: {CSV_PATH}")
    print(f"Images Directory: {IMAGES_DIR}")

    if not IMAGES_DIR.exists():
        print(f"Error: IMAGES_DIR {IMAGES_DIR} does not exist.")
        sys.exit(1)

    # 1. Scan local images
    local_images = []
    total_size = 0
    valid_exts = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
    
    for root, dirs, files in os.walk(IMAGES_DIR):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in valid_exts:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(BASE_DIR)
                rel_to_products = full_path.relative_to(IMAGES_DIR)
                size = full_path.stat().st_size
                total_size += size
                local_images.append({
                    "name": file,
                    "rel_path": rel_path.as_posix(),
                    "rel_to_products": rel_to_products.as_posix(),
                    "folder": rel_to_products.parent.as_posix() if rel_to_products.parent.as_posix() != "." else "root",
                    "size": size
                })

    print(f"Found {len(local_images)} images. Total size: {get_human_size(total_size)} ({total_size} bytes)")

    # Group by folder
    folders = {}
    for img in local_images:
        f = img["folder"]
        folders[f] = folders.get(f, []) + [img]
    
    print("\n--- Image Folders Summary ---")
    for f, imgs in folders.items():
        sub_size = sum(x["size"] for x in imgs)
        print(f"Folder: '{f}' | Images: {len(imgs)} | Size: {get_human_size(sub_size)}")

    # 2. Parse Excel/CSV data
    if not CSV_PATH.exists():
        print(f"CSV path {CSV_PATH} not found.")
        # Find where it is
        csv_files = list(BASE_DIR.glob("**/*.md"))
        print("Available MD files:")
        for f in csv_files[:10]:
            print(f)
        return

    # Let's read lines of CSV
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Let's filter lines of CSV (starting after title/desc header, starting with comma)
    csv_rows = []
    for line in lines:
        if line.strip().startswith(",") or re.match(r"^\s*,", line):
            # Parse CSV row
            reader = csv.reader([line.strip()])
            csv_rows.append(next(reader))
    
    print(f"\nParsed {len(csv_rows)} rows of CSV content.")
    
    # Categorize items
    current_category = None
    products = []
    
    # We will identify category changes by watching for rows with values in columns and empty ID
    # In our CSV:
    # Column 0: always empty
    # Column 1: always empty
    # Column 2: ID or Category name (if ID is missing)
    # Column 3: Name
    # Column 4: Cost
    # Column 5: 1pc or PER KG
    # Column 6: 10pc or other
    
    for row in csv_rows:
        # Clean row: strip elements
        row = [x.strip() for x in row]
        # Skip empty rows
        if not any(row):
            continue
        
        # Check if this row defines a category
        # If row[2] is non-empty and there's no ID in row[2] and the rest of row is empty (or mostly empty)
        # Or if we see headers like "NAME OF THE PRODUCTS", "TREE", "ANKLET", etc.
        val2 = row[2] if len(row) > 2 else ""
        val3 = row[3] if len(row) > 3 else ""
        val4 = row[4] if len(row) > 4 else ""
        val5 = row[5] if len(row) > 5 else ""
        
        # Skip header
        if "NAME OF THE PRODUCTS" in val2 or "NAME OF THE PRODUCTS" in val3:
            current_category = "Gemstone Bracelets"
            continue
        
        if val2 in ["TREE", "ANKLET", "TUMBLE STONE", "ROUGH", "HANGINGS", "ZIBU COINS", "BRACELET CHIP", "PYRAMIDS", "SELENITE PRODUCTS", "TORTOISE", "ANGLES 2 INCH", "PEDANTS", "RING", "CHIPS"]:
            current_category = val2
            continue
        
        # If val2 is a number, it's a product
        if val2.isdigit():
            prod_id = int(val2)
            prod_name = val3
            
            # Extract prices based on category
            price = None
            price_10pc = None
            price_50pc = None
            price_unit = "per piece"
            
            if current_category == "TUMBLE STONE" or current_category == "ROUGH" or current_category == "CHIPS":
                # Price is row[4] (cost or base) and row[5] is per kg
                cost = row[4] if len(row) > 4 else ""
                per_kg = row[5] if len(row) > 5 else ""
                # Some are per piece, some per kg.
                # In TUMBLE STONE, column 4 is "COST", column 5 is "PER KG". Let's check
                # Row: ,,40,Rose,500,650
                price = per_kg if per_kg else cost
                price_unit = "per kg" if per_kg else "per piece"
            elif current_category == "ANKLET":
                # Row: ,,37,DHANYOG,55,180 SINGLE PC /220 PAIR
                # Wait, "180 SINGLE PC /220 PAIR" is under column 4 (cost=55, price=180 single pc / 220 pair)
                price_str = row[4] if len(row) > 4 else ""
                # Let's see: cost is 55, column 4 (which is 1pc price) is 180 SINGLE PC /220 PAIR
                # Let's extract price and units
                # We can store the raw price string in `price` or try to parse it
                price = row[4] if len(row) > 4 else ""
                price_unit = "single/pair"
            else:
                # Column 4 is COST, Column 5 is 1 PC price, Column 6 is 10 PC, Column 7 is 50 PC
                # Row: ,,1,amethyst (N),140,280,230,180
                price = row[4] if len(row) > 4 else "" # wait, index 3 is name, 4 is COST, 5 is 1 PC price, 6 is 10 PC price, 7 is 50 PC price
                price_1pc = row[4] if len(row) > 4 else ""
                # Let's double check columns from row amethyst (N):
                # row is: ['', '', '1', 'amethyst (N)', '140', '280', '230', '180']
                # row[2] = '1'
                # row[3] = 'amethyst (N)'
                # row[4] = '140' (Cost)
                # row[5] = '280' (1 PC price)
                # row[6] = '230' (10 PC price)
                # row[7] = '180' (50 PC price)
                if len(row) > 5:
                    price = row[5]
                if len(row) > 6:
                    price_10pc = row[6]
                if len(row) > 7:
                    price_50pc = row[7]
            
            products.append({
                "id": prod_id,
                "name": prod_name,
                "category": current_category,
                "price": price,
                "price_10pc": price_10pc,
                "price_50pc": price_50pc,
                "price_unit": price_unit,
                "row_raw": row
            })

    print(f"Extracted {len(products)} products from CSV.")

    # Show category counts
    cats = {}
    for p in products:
        cats[p["category"]] = cats.get(p["category"], 0) + 1
    print("\n--- Products Category Summary ---")
    for c, count in cats.items():
        print(f"Category: '{c}' | Products: {count}")

    # Write mapped output
    print("\nMapping images to products...")
    # For mapping:
    # Gemstone Bracelets -> matches root or folder of bracelets (e.g. products)
    # TREE -> matches 'tree photos' folder
    # ANKLET -> matches 'anklet' folder
    # TUMBLE STONE -> matches 'tumble stones' folder
    # SELENITE PRODUCTS -> matches 'selenite charging plates and lamp' folder
    # ZIBU COINS -> matches 'zibu coins' folder
    # CHIPS -> matches 'chips' or 'bead lines' folder
    # HANGINGS -> what folder? Let's check other folders or match in root.
    
    category_folder_map = {
        "Gemstone Bracelets": ["root"],
        "TREE": ["tree photos"],
        "ANKLET": ["anklet"],
        "TUMBLE STONE": ["tumble stones"],
        "SELENITE PRODUCTS": ["selenite charging plates and lamp"],
        "ZIBU COINS": ["zibu coins"],
        "CHIPS": ["chips", "bead lines"],
        # Rest can fall back to searching anywhere or specific directories
    }

    mapped_count = 0
    mapping_results = []

    for p in products:
        p_clean = clean_name(p["name"])
        matched_img = None
        
        # Determine folders to search
        search_folders = category_folder_map.get(p["category"], ["root", "anklet", "bead lines", "chips", "selenite charging plates and lamp", "tree photos", "tumble stones", "zibu coins"])
        
        # Search for a match in the allowed folders
        best_match = None
        for img in local_images:
            if img["folder"] in search_folders or "all" in search_folders:
                img_clean = clean_name(img["name"].split(".")[0])
                # Exact or substring matching
                if p_clean and (p_clean in img_clean or img_clean in p_clean):
                    best_match = img
                    break
        
        # If no match, try searching all folders as fallback
        if not best_match:
            for img in local_images:
                img_clean = clean_name(img["name"].split(".")[0])
                if p_clean and (p_clean in img_clean or img_clean in p_clean):
                    best_match = img
                    break

        if best_match:
            matched_img = best_match["rel_to_products"]
            mapped_count += 1
            # Remove from local_images to prevent double mapping if needed, or keep it.
        
        mapping_results.append({
            "product_id": p["id"],
            "product_name": p["name"],
            "category": p["category"],
            "price": p["price"],
            "price_10pc": p["price_10pc"],
            "price_50pc": p["price_50pc"],
            "price_unit": p["price_unit"],
            "image": matched_img
        })

    print(f"\nSuccessfully mapped {mapped_count} out of {len(products)} products.")

    # Write out a markdown report
    report_path = BASE_DIR / "scripts" / "mapping_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Product to Image Mapping Report\n\n")
        f.write(f"- **Total Products in Spreadsheet:** {len(products)}\n")
        f.write(f"- **Total Mapped Products:** {mapped_count}\n")
        f.write(f"- **Total Unmapped Products:** {len(products) - mapped_count}\n")
        f.write(f"- **Total Images Available:** {len(local_images)}\n")
        f.write(f"- **Total Image Size:** {get_human_size(total_size)} ({total_size} bytes)\n\n")
        
        f.write("## Folder Size Summary\n")
        for folder, imgs in folders.items():
            sub_size = sum(x["size"] for x in imgs)
            f.write(f"- **Folder:** `{folder}` | **Images:** {len(imgs)} | **Size:** {get_human_size(sub_size)}\n")
        
        f.write("\n## Detailed Mapping Table\n\n")
        f.write("| ID | Product Name | Category | Price | Price Unit | Mapped Image |\n")
        f.write("| --- | --- | --- | --- | --- | --- |\n")
        for r in mapping_results:
            img_val = f"`{r['image']}`" if r["image"] else "*BLANK (No Image)*"
            f.write(f"| {r['product_id']} | {r['product_name']} | {r['category']} | {r['price']} | {r['price_unit']} | {img_val} |\n")

    print(f"Report written to {report_path}")

if __name__ == "__main__":
    main()
