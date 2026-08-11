# StoneAura Bracelets — Gemstone Bracelets Website

**Stack:** Django 5.x + Django REST Framework (Backend API) & React.js + Vanilla CSS (Frontend SPA)

For detailed deployment steps, please read the [DEPLOYMENT_GUIDE.md](file:///c:/Users/baps/Desktop/Free%20lance/project%20tushal/StoneAura_Bracelets/DEPLOYMENT_GUIDE.md). For instructions on adding new product images from Google Drive, read the [HOW_TO_ADD_DRIVE_IMAGES.md](file:///c:/Users/baps/Desktop/Free%20lance/project%20tushal/StoneAura_Bracelets/HOW_TO_ADD_DRIVE_IMAGES.md).

---

## Quick Start

### 1. Backend (Django)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run migrations to set up the database
python manage.py migrate

# Seed products and pricing tiers into the database
python manage.py seed_products

# Start the Django development server
python manage.py runserver 8000
```
* The API runs at: **`http://localhost:8000/api/products/`**
* The Admin Dashboard runs at: **`http://localhost:8000/admin/`**

### 2. Frontend (React)
```bash
# Navigate to the frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the React development server
npm start
```
* The local React app runs at: **`http://localhost:3000`**

---

## Project Structure
```
StoneAura_Bracelets/
├── backend/              # Django settings, middleware, and project configuration
├── products/             # Django App (models, views, serializers, and product seed command)
├── frontend/             # React application root
│   ├── public/           # Static public assets (HTML, logos, dynamic product images)
│   └── src/              # React source code
│       ├── components/   # UI elements (Header, Footer, ProductCard, WhatsAppFloat, etc.)
│       └── pages/        # Page-level views (ProductsPage, AdminDashboard)
├── manage.py             # Django project manager CLI
├── requirements.txt      # Python dependencies
└── db.sqlite3            # SQLite database file (gitignored in production)
```

---

## API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/products/` | `GET` | Retrieve all 40 bracelets (supports search, filters, and sorting) |
| `/api/products/?search=amethyst` | `GET` | Search for products by name or description |
| `/api/products/?ordering=price` | `GET` | Sort products by wholesale/retail price |
| `/api/wrist-sizes/` | `GET` | Retrieve available wrist size options |
| `/api/featured/` | `GET` | Retrieve list of featured products |
| `/api/health/` | `GET` | Backend API health-check endpoint |

---

## Security Features

* **CORS Headers**: Configured to restrict external origins (default to localhost:3000 for local development).
* **Rate Limiting**: Automated protection against brute force and scraping (200 requests/min for anonymous users, 500 requests/min for authenticated users).
* **Security Headers**: Standard headers active, including `X-Frame-Options: DENY` and `X-Content-Type-Options: nosniff`.
* **Input Validation**: Strongly typed request validations managed via DRF Serializers.
* **Database Protection**: SQL injection prevention handled automatically by Django ORM queries.
* **XSS Defense**: Escaped outputs handled natively by React's JSX compiler.