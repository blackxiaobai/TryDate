#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Build frontend
cd ../frontend
npm install
npm run build
cd ../backend

# Copy frontend dist to backend
rm -rf frontend-dist
cp -r ../frontend/dist frontend-dist

python manage.py migrate --no-input
python manage.py collectstatic --no-input

# Create admin if not exists
python manage.py shell -c "
from users.models import User
if not User.objects.filter(email='admin@admin.com').exists():
    u = User.objects.create_superuser(email='admin@admin.com', password='admin123')
    u.nickname = '管理员'
    u.gender = 'male'
    u.save()
    print('Admin created')
else:
    print('Admin exists')
"
