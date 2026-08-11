# StoneAura Bracelets — Handoff & Deployment Guide

This project consists of a Django (Python) backend REST API and a React (Single Page Application) frontend. The product data, wholesale pricing tiers, and image associations are served dynamically from a relational database.

---

## Technical Stack
* **Backend**: Django 5.x + Django REST Framework (DRF)
* **Frontend**: React + Vanilla CSS
* **Database**: SQLite (Development/Handoff) — can be swapped to PostgreSQL/MySQL in production
* **Static Assets**: WhiteNoise (efficiently serves frontend files through Django)

---

## 1. Setup and Local Deployment Instructions

### Prerequisites
Make sure you have the following installed on your system:
- **Python 3.10+** (includes `pip`)
- **Node.js 18+** (includes `npm`)

### Step 1: Install Backend dependencies
Open your terminal in the project root directory and install Python dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database and Migrations
Create the SQL database structure by running:
```bash
python manage.py migrate
```

### Step 3: Seed the Product Catalog
Populate the database with all 30 gemstone bracelets, wholesale price tiers, keychain/decor items, and their matching images:
```bash
python manage.py seed_products
```
*Note: The seeding script automatically detects images placed in the `frontend/public/images/products/` folder and matches them to the corresponding database records.*

### Step 4: Build React Frontend Assets
Compile the React source code into optimized, compressed static files that Django can serve:
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Run the compiler:
   ```bash
   npm run build
   ```
   *(This outputs the build files to `frontend/build/`)*
4. Go back to the project root:
   ```bash
   cd ..
   ```

### Step 5: Start the Server
Run the backend web server:
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000`** in your browser to view the running, fully dynamic web application.

---

## 2. Managing Products and Pricing (Django Admin Panel)

You can easily manage your entire catalog (add, delete, edit products, modify wholesale price tiers, update categories) via the Django admin dashboard.

1. **Create an Admin superuser**:
   ```bash
   python manage.py createsuperuser
   ```
2. Follow the terminal prompts to enter a username, email, and password.
3. Start the server and navigate to: **`http://127.0.0.1:8000/admin/`**
4. Log in using the credentials you just created.

---

## 3. Production Deployment Notes

This project supports dynamic configuration for production via environment variables (loaded locally via `.env` or set directly on host providers like Render or Heroku).

### Step 1: Environment Variables
Ensure the following variables are configured in your production hosting panel:
* **`DJANGO_SECRET_KEY`**: A strong, unique secret key for cryptographic signing.
* **`DEBUG`**: Set to `False` in production.
* **`ALLOWED_HOSTS`**: Domain names (comma-separated, e.g. `stoneaura.com,stoneaura.onrender.com`).
* **`DB_NAME`**: Production PostgreSQL database name.
* **`DB_USER`**: PostgreSQL database user.
* **`DB_PASSWORD`**: PostgreSQL database password.
* **`DB_HOST`**: PostgreSQL server hostname.
* **`DB_PORT`**: PostgreSQL connection port (defaults to `5432`).

### Step 2: Database Initialization & Migrations
To build the required database structure in your production PostgreSQL instance:
```bash
python manage.py migrate
```

### Step 3: Seed / Restore Database Content
* To perform a fresh seed of products, categories, and wholesale pricing:
  ```bash
  python manage.py seed_products
  ```
* To restore existing catalog modifications and superuser accounts from a database backup file (e.g., `db_dump.json`):
  ```bash
  # Force UTF-8 decoding if running on Windows PowerShell
  $env:PYTHONUTF8=1; python manage.py loaddata db_dump.json
  ```

### Step 4: Bundle and Serve Static Assets
To collect and bundle all Django and React compiled static assets into `staticfiles/`:
```bash
python manage.py collectstatic --no-input
```
django uses **WhiteNoise** middleware to serve these compiled assets efficiently in production.

