#!/bin/bash
# entrypoint.sh

# Wait for the database to be ready
echo "Waiting for database..."
until nc -z -v -w30 db 5432; do
  echo "Waiting for database connection..."
  sleep 1
done

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "Checking if superuser exists..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "adminpassword")
    print("Superuser created.")
else:
    print("Superuser already exists.")
EOF

# Start Gunicorn server
echo "Starting server..."
gunicorn wsgi:application --bind 0.0.0.0:8001
