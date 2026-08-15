import os
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Upload renamed Title Case local images from mapping_report.md to ImageKit.io and update DB URLs."

    def handle(self, *args, **options):
        private_key = os.environ.get("IMAGEKIT_PRIVATE_KEY")
        url_endpoint = os.environ.get("IMAGEKIT_URL_ENDPOINT")

        if not private_key or not url_endpoint:
            self.stdout.write(self.style.ERROR(
                "Error: IMAGEKIT_PRIVATE_KEY and IMAGEKIT_URL_ENDPOINT are not set in the environment variables.\n"
                "Please add them to your .env file first."
            ))
            return

        base_dir = Path(settings.BASE_DIR)
        report_path = base_dir / "mapping_report.md"
        local_dir = base_dir / "frontend" / "public" / "images" / "products"

        if not report_path.exists():
            self.stdout.write(self.style.ERROR(f"Error: {report_path} not found! Run mapping generator first."))
            return

        # 1. Parse mapping_report.md to find renamed images and their product IDs
        renamed_images = [] # list of (product_id, renamed_rel_path)
        
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
                        renamed_images.append((prod_id, new_img))

        total = len(renamed_images)
        if total == 0:
            self.stdout.write(self.style.SUCCESS("No renamed images found in mapping report to upload."))
            return

        self.stdout.write(f"Found {total} renamed images to upload. Starting ImageKit migration...")

        success_count = 0
        failed_count = 0
        db_updates_count = 0

        # API upload endpoint
        upload_url = "https://upload.imagekit.io/api/v1/files/upload"
        auth = HTTPBasicAuth(private_key, "")

        for i, (prod_id, rel_path) in enumerate(renamed_images, 1):
            local_path = local_dir / rel_path
            filename = os.path.basename(rel_path)
            # Folder inside ImageKit: upload all products directly under /products
            folder_name = "/products"

            self.stdout.write(f"[{i}/{total}] Uploading '{rel_path}' to ImageKit folder '{folder_name}'...")

            if not local_path.exists():
                self.stdout.write(self.style.ERROR(f"  [ERROR] Local file not found: {local_path}"))
                failed_count += 1
                continue

            try:
                # Open and read file bytes
                with open(local_path, "rb") as f:
                    file_data = f.read()

                files = {
                    'file': (filename, file_data)
                }
                data = {
                    'fileName': filename,
                    'folder': folder_name,
                    'useUniqueFileName': 'false'  # Clean URLs
                }

                response = requests.post(upload_url, auth=auth, files=files, data=data, timeout=45)
                
                if response.status_code == 200:
                    cloud_url = response.json().get("url")
                    self.stdout.write(self.style.SUCCESS(f"  [OK] Uploaded! URL: {cloud_url}"))
                    success_count += 1

                    # Update product in database
                    try:
                        product = Product.objects.get(id=prod_id)
                        product.image_url = cloud_url
                        product.save()
                        self.stdout.write(self.style.SUCCESS(f"    [DB UPDATE] Updated DB for product: {product.name} (ID: {prod_id})"))
                        db_updates_count += 1
                    except Product.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"    [DB SKIP] Product with ID {prod_id} not found in database (skipped update)"))
                else:
                    self.stdout.write(self.style.ERROR(
                        f"  [FAIL] Failed: API returned status {response.status_code} - {response.text}"
                    ))
                    failed_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  [ERROR] Error uploading: {e}"))
                failed_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nImageKit migration complete!\n"
            f"Successfully uploaded: {success_count}\n"
            f"Failed/Missing: {failed_count}\n"
            f"Database products updated: {db_updates_count}\n"
        ))
