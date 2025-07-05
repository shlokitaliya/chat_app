#!/usr/bin/env bash
# Install npm dependencies and build Tailwind CSS
npm install
npm run build

# Run Django collectstatic to gather static files
python manage.py collectstatic --noinput
