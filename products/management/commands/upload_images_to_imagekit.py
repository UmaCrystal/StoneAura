import os
import re
from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from django.conf import settings
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Recursively upload all product images from frontend/public/images/products to ImageKit.io preserving folder structure and update database records."

    def handle(self, *args, **options):
        # Explicitly load .env from BASE_DIR
        base_dir = Path(settings.BASE_DIR)
        load_dotenv(base_dir / '.env')

        private_key = os.environ.get("IMAGEKIT_PRIVATE_KEY")
        url_endpoint = os.environ.get("IMAGEKIT_URL_ENDPOINT")

        if not private_key or not url_endpoint:
            self.stdout.write(self.style.ERROR(
                "Error: IMAGEKIT_PRIVATE_KEY and IMAGEKIT_URL_ENDPOINT are not set in environment variables.\n"
                "Please check your .env file."
            ))
            return

        local_dir = base_dir / "frontend" / "public" / "images" / "products"
        if not local_dir.exists():
            self.stdout.write(self.style.ERROR(f"Error: Local directory does not exist at {local_dir}"))
            return

        valid_extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
        files_to_upload = []

        for root, _, files in os.walk(local_dir):
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in valid_extensions:
                    full_path = Path(root) / file
                    rel_path = full_path.relative_to(local_dir)
                    subfolder = rel_path.parent.as_posix()
                    
                    if subfolder == ".":
                        ik_folder = "/products"
                    else:
                        # Clean spaces & special chars for ImageKit folder parameter
                        clean_subfolder = re.sub(r'[^a-zA-Z0-9_\-/]', '_', subfolder)
                        clean_subfolder = re.sub(r'_+', '_', clean_subfolder).strip('_')
                        ik_folder = f"/products/{clean_subfolder}"
                    
                    files_to_upload.append({
                        "filename": file,
                        "full_path": full_path,
                        "rel_path": rel_path.as_posix(),
                        "subfolder": subfolder,
                        "ik_folder": ik_folder,
                    })

        total = len(files_to_upload)
        if total == 0:
            self.stdout.write(self.style.SUCCESS("No image files found in 'frontend/public/images/products/'."))
            return

        self.stdout.write(f"Found {total} image files across root and subfolders. Starting upload to ImageKit.io...\n")

        success_count = 0
        failed_count = 0
        linked_products_count = 0

        upload_url = "https://upload.imagekit.io/api/v1/files/upload"
        auth = HTTPBasicAuth(private_key, "")

        for i, item in enumerate(files_to_upload, 1):
            filename = item["filename"]
            full_path = item["full_path"]
            ik_folder = item["ik_folder"]
            rel_path = item["rel_path"]

            self.stdout.write(f"[{i}/{total}] Uploading '{rel_path}' -> ImageKit '{ik_folder}'...")

            try:
                with open(full_path, "rb") as f:
                    file_data = f.read()

                files = {
                    'file': (filename, file_data)
                }
                data = {
                    'fileName': filename,
                    'folder': ik_folder,
                    'useUniqueFileName': 'false'
                }

                response = requests.post(upload_url, auth=auth, files=files, data=data, timeout=45)

                if response.status_code == 200:
                    cloud_url = response.json().get("url")
                    self.stdout.write(self.style.SUCCESS(f"  [OK] Uploaded! URL: {cloud_url}"))
                    success_count += 1

                    # Look up matching product in database by image_url filename
                    matching_products = Product.objects.filter(
                        image_url__icontains=filename
                    )

                    if matching_products.exists():
                        p_names = []
                        for product in matching_products:
                            product.image_url = cloud_url
                            product.save()
                            p_names.append(product.name)
                            linked_products_count += 1
                        self.stdout.write(self.style.SUCCESS(f"     Linked DB product(s): {', '.join(p_names)}"))
                    else:
                        self.stdout.write(self.style.WARNING("     Uploaded to ImageKit (not linked directly to DB product)"))
                else:
                    self.stdout.write(self.style.ERROR(
                        f"  [FAIL] Status {response.status_code} - {response.text}"
                    ))
                    failed_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  [FAIL] Error uploading: {e}"))
                failed_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nUpload process finished!\n"
            f"Successfully uploaded: {success_count}\n"
            f"Failed: {failed_count}\n"
            f"Database products updated: {linked_products_count}\n"
        ))
