#!/bin/bash

# Apply migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create a superuser if it doesn't exist
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='admin').exists() or \
User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" \
| python manage.py shell

# Start Daphne server
exec daphne -b 0.0.0.0 -p 8000 chatapp.asgi:application
