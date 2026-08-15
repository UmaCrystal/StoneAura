import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "frontend" / "public" / "images" / "products"

def main():
    print(f"Scanning subdirectories of {IMAGES_DIR}...")
    valid_exts = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
    
    # List files in root first
    root_files = []
    for file in os.listdir(IMAGES_DIR):
        full_path = IMAGES_DIR / file
        if full_path.is_file() and full_path.suffix.lower() in valid_exts:
            root_files.append(file)
    print(f"\n[Root Folder] - Contains {len(root_files)} images (mostly Bracelets):")
    for f in sorted(root_files):
        print(f"  - {f}")
        
    # List files in each sub-directory
    for root, dirs, files in os.walk(IMAGES_DIR):
        if root == str(IMAGES_DIR):
            continue
        rel_dir = Path(root).relative_to(IMAGES_DIR).as_posix()
        dir_files = [f for f in files if os.path.splitext(f)[1].lower() in valid_exts]
        if dir_files:
            print(f"\n[{rel_dir}] - Contains {len(dir_files)} images:")
            for f in sorted(dir_files):
                print(f"  - {f}")

if __name__ == "__main__":
    main()
