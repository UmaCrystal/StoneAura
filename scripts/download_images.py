"""
download_images.py
==================
One-time script: downloads every product image from a public Google Drive
folder and saves them to  frontend/public/images/products/

Usage:
    python download_images.py <FOLDER_ID>

Where FOLDER_ID is the long ID in the Drive folder URL:
    https://drive.google.com/drive/folders/FOLDER_ID

Requirements:
    pip install requests

All files are saved as  <sanitised_name>.<ext>  and the script prints the
final mapping so you can paste the filenames directly into seed_products.py.
"""

import sys
import re
import os
import pathlib
import urllib.parse

try:
    import requests
except ImportError:
    sys.exit("Missing dependency. Run:  pip install requests")


# ── helpers ─────────────────────────────────────────────────────────────────

DEST = pathlib.Path(__file__).parent.parent / "frontend" / "public" / "images" / "products"
DEST.mkdir(parents=True, exist_ok=True)

FOLDER_API = "https://www.googleapis.com/drive/v3/files"
DOWNLOAD   = "https://drive.google.com/uc?export=download&id={}"


def sanitise(name: str) -> str:
    """Lower-case, spaces → hyphens, strip non-alphanumeric (keep hyphens/dots)."""
    name = name.lower().strip()
    name = re.sub(r"[^\w.\-]+", "-", name)
    name = re.sub(r"-{2,}", "-", name)
    return name.strip("-")


def list_folder(folder_id: str, api_key: str | None) -> list[dict]:
    """
    List files in a *public* Drive folder.
    Works without an API key via the web-scrape approach if no key given.
    """
    params = {
        "q": f"'{folder_id}' in parents and trashed=false",
        "fields": "files(id,name,mimeType)",
        "pageSize": 200,
    }
    if api_key:
        params["key"] = api_key

    url = FOLDER_API
    r = requests.get(url, params=params, timeout=20)
    if r.status_code == 200:
        return r.json().get("files", [])

    # Fallback: scrape the public folder HTML for file IDs
    print("  API key not supplied or quota exceeded — using HTML scrape fallback.")
    folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
    html = requests.get(folder_url, timeout=20).text
    # Drive embeds file IDs in data-id attributes
    ids   = re.findall(r'"([\w-]{28,})"', html)
    names = re.findall(r'data-tooltip="([^"]+)"', html)
    return [{"id": i, "name": n, "mimeType": "image/*"}
            for i, n in zip(ids, names) if i and n]


def download_file(file_id: str, dest_path: pathlib.Path) -> bool:
    url = DOWNLOAD.format(file_id)
    session = requests.Session()
    r = session.get(url, stream=True, timeout=30)

    # Handle Drive's large-file confirmation page
    token = None
    for k, v in r.cookies.items():
        if k.startswith("download_warning"):
            token = v
            break

    if token:
        r = session.get(url, params={"confirm": token}, stream=True, timeout=30)

    if r.status_code != 200:
        return False

    with open(dest_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=32_768):
            f.write(chunk)
    return True


# ── main ────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    folder_id = sys.argv[1].strip()
    api_key   = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"\n[Folder] Listing folder: {folder_id}")
    files = list_folder(folder_id, api_key)

    if not files:
        print("Error: No files found. Make sure the folder is set to 'Anyone with the link'.")
        sys.exit(1)

    image_mime = {"image/jpeg", "image/png", "image/webp", "image/gif", "image/*"}
    image_files = [f for f in files if any(m in f.get("mimeType", "") for m in ["image"])]
    print(f"[Images] Found {len(image_files)} image(s). Downloading...\n")

    mapping: list[tuple[str, str]] = []   # (original_name, local_filename)

    import shutil

    for f in image_files:
        orig_name  = f["name"]
        file_id    = f["id"]
        # preserve original extension
        ext = pathlib.Path(orig_name).suffix or ".jpg"
        local_name = sanitise(pathlib.Path(orig_name).stem) + ext
        dest       = DEST / local_name

        # Ensure we copy to build folder if build directory exists
        build_dest_dir = pathlib.Path(__file__).parent.parent / "frontend" / "build" / "images" / "products"
        has_build = (pathlib.Path(__file__).parent.parent / "frontend" / "build").exists()
        if has_build:
            build_dest_dir.mkdir(parents=True, exist_ok=True)

        if dest.exists():
            print(f"  [cached]  {local_name}")
            mapping.append((orig_name, local_name))
            if has_build:
                build_dest = build_dest_dir / local_name
                if not build_dest.exists() or build_dest.stat().st_size != dest.stat().st_size:
                    shutil.copy2(dest, build_dest)
            continue

        ok = download_file(file_id, dest)
        if ok:
            size_kb = dest.stat().st_size // 1024
            print(f"  [ok]  {local_name}  ({size_kb} KB)")
            mapping.append((orig_name, local_name))
            if has_build:
                shutil.copy2(dest, build_dest_dir / local_name)
        else:
            print(f"  [fail]    {orig_name}  (id={file_id})")

    print(f"\n\n{'='*60}")
    print("Download complete. Add these to seed_products.py:\n")
    print('# Image filename → local path mapping')
    print('IMG = {')
    for orig, local in sorted(mapping, key=lambda x: x[1]):
        key = pathlib.Path(local).stem.upper().replace("-", "_")
        print(f'    "{key}": "{local}",')
    print('}')
    print(f"\n{'='*60}")
    print("Then run:  python manage.py seed_products\n")


if __name__ == "__main__":
    main()
