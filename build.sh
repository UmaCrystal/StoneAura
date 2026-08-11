#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Seed database if requested
if [ "$SEED_DATABASE" = "true" ]; then
    echo "SEED_DATABASE is set to true. Seeding products database..."
    python manage.py seed_products
fi
