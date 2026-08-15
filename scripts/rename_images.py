import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_PATH = BASE_DIR / "mapping_report.md"
IMAGES_DIR = BASE_DIR / "frontend" / "public" / "images" / "products"

def main():
    print(f"Renaming images based on mapping report at {REPORT_PATH}...")
    if not REPORT_PATH.exists():
        print(f"Error: {REPORT_PATH} not found!")
        return

    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    rename_ops = []
    
    # Simple markdown table parser
    for line in lines:
        if line.strip().startswith("|") and not line.strip().startswith("| ---"):
            parts = [p.strip() for p in line.split("|")]
            # Table row structure:
            # parts[0] is empty (due to leading '|')
            # parts[1] is ID
            # parts[2] is Excel Product Name
            # parts[3] is Category
            # parts[4] is Price
            # parts[5] is Original Image Path
            # parts[6] is Proposed Renamed Image Path
            if len(parts) >= 7 and parts[1].isdigit():
                orig_raw = parts[5].strip()
                new_raw = parts[6].strip()
                
                # Strip backticks
                orig_img = orig_raw.replace("`", "") if orig_raw else ""
                new_img = new_raw.replace("`", "") if new_raw else ""
                
                if orig_img and new_img and orig_img != "*BLANK*" and new_img != "*BLANK*":
                    rename_ops.append((orig_img, new_img))

    print(f"Found {len(rename_ops)} image rename operations in mapping report.")

    success_count = 0
    fail_count = 0

    for orig, new in rename_ops:
        src_path = IMAGES_DIR / orig
        dst_path = IMAGES_DIR / new

        # Check if source file exists
        if not src_path.exists():
            # Maybe it has already been renamed? Check if destination already exists
            if dst_path.exists():
                print(f"  [ALREADY DONE] {orig} -> {new}")
                success_count += 1
            else:
                print(f"  [ERROR] Source image not found: {src_path}")
                fail_count += 1
            continue

        try:
            # Ensure destination directory exists (if nested)
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Rename file
            os.rename(src_path, dst_path)
            print(f"  [OK] Renamed: {orig} -> {new}")
            success_count += 1
        except Exception as e:
            print(f"  [FAIL] Failed renaming {orig} to {new}: {e}")
            fail_count += 1

    print(f"\nRenaming process complete! Successes: {success_count}, Failures/Missing: {fail_count}")

if __name__ == "__main__":
    main()
