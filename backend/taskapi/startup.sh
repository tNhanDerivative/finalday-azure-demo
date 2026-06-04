#!/usr/bin/env bash
set -e

# Ensure relative paths resolve correctly when App Service launches this script
# from the deployment root.
cd "$(dirname "$0")"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn taskapi.wsgi:application --bind=0.0.0.0:${PORT:-8000}
