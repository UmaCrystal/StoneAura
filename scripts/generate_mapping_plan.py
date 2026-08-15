import os
import csv
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = Path(r"C:\Users\baps\.gemini\antigravity-ide\brain\bd07581c-f9a8-4b1f-bce2-5a586ca969d5\.system_generated\steps\19\content.md")
IMAGES_DIR = BASE_DIR / "frontend" / "public" / "images" / "products"

def get_clean_keywords(name):
    """Normalize a name and split it into clean lowercase keywords with spelling overrides."""
    if not name:
        return []
    # Remove things like (N), (D), (n), (d)
    name = re.sub(r"\s*\([NDnd]\)\s*", " ", name)
    name = name.lower()
    
    # Spelling corrections
    spelling_fixes = {
        "carnilane": "carnelian",
        "quatz": "quartz",
        "tourmuline": "tourmaline",
        "obsedian": "obsidian",
        "appetitte": "apatite",
        "torquoise": "turquoise",
        "charka": "chakra",
        "yello": "yellow",
        "garnate": "garnet",
        "rhodonote": "rhodonite"
    }
    for orig, fix in spelling_fixes.items():
        name = name.replace(orig, fix)
        
    # Replace non-alphanumeric with spaces
    name = re.sub(r"[^\w\s]", " ", name)
    return [w for w in name.split() if w not in ["n", "d", "pc", "pcs", "single", "pair", "with", "and", "or"]]

def clean_file_basename(filename):
    """Clean image filename for keyword comparison with spelling overrides."""
    base = os.path.splitext(filename)[0].lower()
    base = re.sub(r"\s*-\s*", " ", base)
    base = re.sub(r"[^\w\s]", " ", base)
    
    spelling_fixes = {
        "carnilane": "carnelian",
        "quatz": "quartz",
        "tourmuline": "tourmaline",
        "obsedian": "obsidian",
        "appetitte": "apatite",
        "torquoise": "turquoise",
        "charka": "chakra",
        "yello": "yellow",
        "garnate": "garnet",
        "rhodonote": "rhodonite"
    }
    for orig, fix in spelling_fixes.items():
        base = base.replace(orig, fix)
        
    return base

def to_title_case(name):
    """Capitalize the first letter of each word."""
    # Split name by space/hyphen and capitalize first letter
    words = re.split(r"(\s+)", name.strip())
    title_words = []
    for w in words:
        if w.strip():
            title_words.append(w[0].upper() + w[1:].lower())
        else:
            title_words.append(w)
    return "".join(title_words)

def main():
    print("Generating refined mapping plan...")
    
    # 1. Read all local images on disk
    valid_exts = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
    local_images = []
    
    for root, dirs, files in os.walk(IMAGES_DIR):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in valid_exts:
                full_path = Path(root) / file
                rel_to_products = full_path.relative_to(IMAGES_DIR)
                folder = rel_to_products.parent.as_posix()
                if folder == ".":
                    folder = "root"
                
                # Tag if it is a tree image
                is_tree_img = "tree" in file.lower() or folder == "tree photos"
                
                local_images.append({
                    "filename": file,
                    "ext": ext,
                    "rel_path": rel_to_products.as_posix(),
                    "folder": folder,
                    "full_path": full_path,
                    "size": full_path.stat().st_size,
                    "is_tree_img": is_tree_img
                })

    print(f"Loaded {len(local_images)} image assets.")

    # 2. Parse Excel/CSV data
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    csv_rows = []
    for line in lines:
        if line.strip().startswith(",") or re.match(r"^\s*,", line):
            reader = csv.reader([line.strip()])
            csv_rows.append(next(reader))
            
    products = []
    current_category = None
    
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
            price = ""
            price_10pc = ""
            price_50pc = ""
            price_unit = "per piece"
            
            if current_category == "TUMBLE STONE" or current_category == "ROUGH" or current_category == "CHIPS":
                cost = row[4] if len(row) > 4 else ""
                per_kg = row[5] if len(row) > 5 else ""
                price = per_kg if per_kg else cost
                price_unit = "per kg" if per_kg else "per piece"
            elif current_category == "ANKLET":
                price = row[4] if len(row) > 4 else ""
                price_unit = "single/pair"
            else:
                if len(row) > 5:
                    price = row[5]
                if len(row) > 6:
                    price_10pc = row[6]
                if len(row) > 7:
                    price_50pc = row[7]

            FRONTEND_CATEGORIES = {
                "Gemstone Bracelets": "Gemstone Bracelets",
                "TREE": "Gemstone Tree",
                "ANKLET": "Anklets",
                "TUMBLE STONE": "Tumbled Stones",
                "ROUGH": "Rough Stone",
                "HANGINGS": "Unique Products",
                "ZIBU COINS": "Zibu Coin",
                "BRACELET CHIP": "Tumbled Bracelets",
                "PYRAMIDS": "Pyramid Stone",
                "SELENITE PRODUCTS": "Selenite Stone",
                "TORTOISE": "Unique Products",
                "ANGLES 2 INCH": "Gemstone Angels",
                "PEDANTS": "Gemstone Pendant",
                "RING": "Gemstone",
                "CHIPS": "Healing Crystals"
            }
            
            frontend_cat = FRONTEND_CATEGORIES.get(current_category, current_category)
            
            products.append({
                "id": prod_id,
                "name": prod_name,
                "excel_category": current_category,
                "frontend_category": frontend_cat,
                "price": price,
                "price_10pc": price_10pc,
                "price_50pc": price_50pc,
                "price_unit": price_unit,
            })

    # Group images by folder for faster folder-specific matching
    images_by_folder = {}
    for img in local_images:
        images_by_folder[img["folder"]] = images_by_folder.get(img["folder"], []) + [img]

    category_folders = {
        "Gemstone Bracelets": ["root"],
        "TREE": ["tree photos"],
        "ANKLET": ["anklet"],
        "TUMBLE STONE": ["tumble stones"],
        "ZIBU COINS": ["zibu coins"],
        "CHIPS": ["chips"],
        "BRACELET CHIP": ["root"],
        "SELENITE PRODUCTS": ["selenite charging plates and lamp"],
    }

    final_mapping = []
    mapped_images_set = set()

    for p in products:
        p_name = p["name"]
        cat = p["excel_category"]
        p_kws = get_clean_keywords(p_name)
        
        # Decide which folders are relevant (default to empty list if no folder exists on disk)
        target_folders = category_folders.get(cat, [])
        
        best_match = None
        
        # Try matching in the specific category folders first
        for folder in target_folders:
            imgs = images_by_folder.get(folder, [])
            for img in imgs:
                # Rule: Bracelets (except TREE) must not match tree images
                if cat == "Gemstone Bracelets" and img["is_tree_img"]:
                    continue
                if cat != "TREE" and img["is_tree_img"]:
                    continue
                    
                img_base = clean_file_basename(img["filename"])
                # Match if all product keywords are in the image filename
                if p_kws and all(kw in img_base for kw in p_kws):
                    best_match = img
                    break
            if best_match:
                break
                
        # If no specific match, try a loose substring match in target folders
        if not best_match:
            for folder in target_folders:
                imgs = images_by_folder.get(folder, [])
                for img in imgs:
                    if cat == "Gemstone Bracelets" and img["is_tree_img"]:
                        continue
                    if cat != "TREE" and img["is_tree_img"]:
                        continue
                        
                    img_base = clean_file_basename(img["filename"])
                    p_clean = " ".join(p_kws)
                    if p_clean and (p_clean in img_base or img_base in p_clean):
                        best_match = img
                        break
                if best_match:
                    break

        # We search strictly in the target folders for the category with NO fallbacks to other folders.
        # This prevents bracelets from mapping to bead lines, tumble stones, or other nested folder images.
        # Done.

        # Special manual override corrections for edge cases
        # E.g. DHANYOG is Money Magnet
        if not best_match and "dhanyog" in p_name.lower():
            if cat == "ANKLET":
                # Find money magnet anklet
                for img in images_by_folder.get("anklet", []):
                    if "money magnet" in img["filename"].lower():
                        best_match = img
                        break
            elif cat == "Gemstone Bracelets":
                # Dhanyog is Money Magnet
                for img in images_by_folder.get("root", []):
                    if "money magnet" in img["filename"].lower() and not img["is_tree_img"]:
                        best_match = img
                        break
            elif cat == "BRACELET CHIP":
                # No specific image, but we can search for chip images
                pass

        if not best_match and ("seven charka" in p_name.lower() or "7 charka" in p_name.lower() or "seven chakra" in p_name.lower() or "7 chakra" in p_name.lower()):
            if cat == "Gemstone Bracelets":
                # Find seven chakra bracelet
                for img in images_by_folder.get("root", []):
                    if "seven chakra" in img["filename"].lower() and not img["is_tree_img"]:
                        best_match = img
                        break

        # If we found a match, generate the new clean Title Case filename
        new_filename = None
        new_rel_path = None
        if best_match:
            # Format: [Product Name][Ext] in Title Case, e.g. "Amethyst Bracelet.jpg"
            # Add category suffix if needed to distinguish, or just keep it simple
            # Let's check category suffix to make it descriptive
            suffix = ""
            if cat == "TREE":
                suffix = " Tree"
            elif cat == "ANKLET":
                suffix = " Anklet"
            elif cat == "TUMBLE STONE":
                suffix = " Tumble Stone"
            elif cat == "ZIBU COINS":
                suffix = " Zibu Coin"
            elif cat == "CHIPS":
                suffix = " Chips"
            elif cat == "SELENITE PRODUCTS":
                suffix = ""  # Already has descriptive names like round plate/bowl/lamp
            elif cat == "Gemstone Bracelets":
                suffix = " Bracelet"
                
            clean_base = re.sub(r"\s*\([NDnd]\)\s*", "", p_name)
            clean_base = re.sub(r"[^\w\s\-]", "", clean_base).strip()
            
            # Ensure it ends with bracelet/tree etc. without duplicating it
            if suffix and not clean_base.lower().endswith(suffix.lower().strip()):
                formatted_name = f"{clean_base}{suffix}"
            else:
                formatted_name = clean_base
                
            new_filename = to_title_case(formatted_name) + best_match["ext"]
            # Subdirectory path relative to products folder
            if best_match["folder"] != "root":
                new_rel_path = f"{best_match['folder']}/{new_filename}"
            else:
                new_rel_path = new_filename
                
            mapped_images_set.add(best_match["rel_path"])

        final_mapping.append({
            "product_id": p["id"],
            "excel_name": p["name"],
            "category": p["frontend_category"],
            "price": p["price"],
            "price_10pc": p["price_10pc"],
            "price_50pc": p["price_50pc"],
            "price_unit": p["price_unit"],
            "original_image": best_match["rel_path"] if best_match else None,
            "original_folder": best_match["folder"] if best_match else None,
            "new_filename": new_filename,
            "new_rel_path": new_rel_path
        })

    # Find unmapped images
    unmapped_images = []
    for img in local_images:
        if img["rel_path"] not in mapped_images_set:
            unmapped_images.append(img)

    # Write report
    report_path = BASE_DIR / "mapping_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Refined Product to Image Mapping & Renaming Plan\n\n")
        f.write(f"- **Total Products in Spreadsheet:** {len(products)}\n")
        f.write(f"- **Mapped Products:** {len([x for x in final_mapping if x['original_image']])}\n")
        f.write(f"- **Unmapped Products (Blank Images):** {len([x for x in final_mapping if not x['original_image']])}\n")
        f.write(f"- **Total Local Images:** {len(local_images)}\n")
        f.write(f"- **Unmapped Local Images:** {len(unmapped_images)}\n\n")
        
        f.write("## Proposed Renaming & Mapping Table\n\n")
        f.write("| ID | Excel Product Name | Excel Category | Price (Unit) | Original Image Path | Proposed Renamed Image Path |\n")
        f.write("| --- | --- | --- | --- | --- | --- |\n")
        for m in final_mapping:
            orig = f"`{m['original_image']}`" if m["original_image"] else "*BLANK*"
            new = f"`{m['new_rel_path']}`" if m["new_rel_path"] else "*BLANK*"
            price_str = f"₹{m['price']}" if m['price'] else "Blank"
            if m['price_unit'] != "per piece":
                price_str += f" ({m['price_unit']})"
            f.write(f"| {m['product_id']} | {m['excel_name']} | {m['category']} | {price_str} | {orig} | {new} |\n")

        f.write("\n## Unmapped Images (Not Linked to Spreadsheet Products)\n")
        f.write("These images were found in the public folder but did not match any spreadsheet row:\n\n")
        f.write("| Folder | Filename | Size |\n")
        f.write("| --- | --- | --- |\n")
        for img in sorted(unmapped_images, key=lambda x: (x["folder"], x["filename"])):
            size_kb = f"{img['size'] / 1024:.2f} KB"
            f.write(f"| `{img['folder']}` | `{img['filename']}` | {size_kb} |\n")

    print(f"Refined report written to {report_path}")

if __name__ == "__main__":
    main()
