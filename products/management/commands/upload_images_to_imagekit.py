import os
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Upload all local product images starting with /images/products/ to ImageKit.io and update database records."

    def handle(self, *args, **options):
        private_key = os.environ.get("IMAGEKIT_PRIVATE_KEY")
        url_endpoint = os.environ.get("IMAGEKIT_URL_ENDPOINT")

        if not private_key or not url_endpoint:
            self.stdout.write(self.style.ERROR(
                "Error: IMAGEKIT_PRIVATE_KEY and IMAGEKIT_URL_ENDPOINT are not set in the environment variables.\n"
                "Please add them to your .env file first."
            ))
            return

        local_dir = os.path.join(settings.BASE_DIR, "frontend", "public", "images", "products")
        if not os.path.exists(local_dir):
            self.stdout.write(self.style.ERROR(f"Error: Local directory does not exist at {local_dir}"))
            return

        # List all valid image files in the directory
        valid_extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
        files_to_upload = [
            f for f in os.listdir(local_dir)
            if os.path.isfile(os.path.join(local_dir, f)) and os.path.splitext(f)[1].lower() in valid_extensions
        ]

        total = len(files_to_upload)
        if total == 0:
            self.stdout.write(self.style.SUCCESS("No image files found in 'frontend/public/images/products/'."))
            return

        self.stdout.write(f"Found {total} image files on disk. Starting upload to ImageKit.io...")

        success_count = 0
        failed_count = 0
        linked_products_count = 0

        # API upload endpoint
        upload_url = "https://upload.imagekit.io/api/v1/files/upload"
        auth = HTTPBasicAuth(private_key, "")

        for i, filename in enumerate(files_to_upload, 1):
            local_path = os.path.join(local_dir, filename)
            self.stdout.write(f"[{i}/{total}] Uploading file '{filename}'...")

            try:
                # Open and read file contents
                with open(local_path, "rb") as f:
                    file_data = f.read()

                files = {
                    'file': (filename, file_data)
                }
                data = {
                    'fileName': filename,
                    'folder': '/products',
                    'useUniqueFileName': 'false'  # keep filenames clean on ImageKit
                }

                response = requests.post(upload_url, auth=auth, files=files, data=data, timeout=45)
                
                if response.status_code == 200:
                    cloud_url = response.json().get("url")
                    self.stdout.write(self.style.SUCCESS(f"  ✓ Uploaded to ImageKit! URL: {cloud_url}"))
                    success_count += 1

                    # Look up and update any matching products in the database
                    matching_products = Product.objects.filter(
                        image_url__endswith="/" + filename
                    )
                    
                    if matching_products.exists():
                        p_names = []
                        for product in matching_products:
                            product.image_url = cloud_url
                            product.save()
                            p_names.append(product.name)
                            linked_products_count += 1
                        self.stdout.write(self.style.SUCCESS(f"    ↳ Linked database product(s): {', '.join(p_names)}"))
                    else:
                        self.stdout.write(self.style.WARNING("    ↳ Not linked to any database product (uploaded to ImageKit only)"))
                else:
                    self.stdout.write(self.style.ERROR(
                        f"  ✗ Failed: API returned status {response.status_code} - {response.text}"
                    ))
                    failed_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Error uploading: {e}"))
                failed_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nUpload complete!\n"
            f"Successfully uploaded files: {success_count}\n"
            f"Failed uploads: {failed_count}\n"
            f"Database products updated: {linked_products_count}"
        ))

        if success_count > 0:
            self.stdout.write(self.style.SUCCESS(
                "\nAll images are uploaded to ImageKit.io! "
                "You can now safely delete the local product images from 'frontend/public/images/products/'!"
            ))

