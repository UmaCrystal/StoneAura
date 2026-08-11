# StoneAura Workspace Rules & Memory

This file preserves the deployment, database, and image configurations of the StoneAura project.

## 1. Tech Stack & Services
* **Frontend:** React SPA (Vanilla CSS) hosted on **Vercel**.
* **Backend:** Django 5.x + DRF hosted on **Render**.
* **Database:** Serverless PostgreSQL hosted on **Neon.tech** (configured dynamically via `DATABASE_URL` in `.env` using `dj-database-url`).
* **Image Hosting:** Cloud-hosted on **ImageKit.io** (free tier up to 20 GB).

---

## 2. Image Management (ImageKit.io)
* **Status:** All local product images have been fully migrated to ImageKit.io and removed from the Git repository/codebase.
* **Database URLs:** All product records in the database use cloud-hosted `https://ik.imagekit.io/...` URLs.
* **Persistent Uploads Fallback:** When adding or updating products via the Django Admin panel or backend APIs, `products/views.py` automatically uploads files to ImageKit if `IMAGEKIT_PRIVATE_KEY` and `IMAGEKIT_URL_ENDPOINT` are set in the environment.

---

## 3. Key Commands
* **Seeding the Database:** Run `python manage.py seed_products` to seed exactly the **30 main bracelets** and **4 accessory/selenite items** with correct wholesale prices.
* **Cloud Migration Utility:** Run `python manage.py upload_images_to_imagekit` if you ever put new local images in `frontend/public/images/products/` and want to migrate them to ImageKit.io and update database URLs.
