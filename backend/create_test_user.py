import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bugtrace.settings')
django.setup()

# Import Django models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create a test user if it doesn't exist
username = 'testuser'
email = 'test@example.com'
password = 'testpassword'

if not User.objects.filter(username=username).exists():
    user = User.objects.create_user(username=username, email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    print(f"Created test user: {username}")
    print(f"Token: {token.key}")
else:
    user = User.objects.get(username=username)
    token, _ = Token.objects.get_or_create(user=user)
    print(f"Test user already exists: {username}")
    print(f"Token: {token.key}")

# Create an admin user if it doesn't exist
admin_username = 'admin'
admin_email = 'admin@example.com'
admin_password = 'adminpassword'

if not User.objects.filter(username=admin_username).exists():
    admin = User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
    token, _ = Token.objects.get_or_create(user=admin)
    print(f"Created admin user: {admin_username}")
    print(f"Token: {token.key}")
else:
    admin = User.objects.get(username=admin_username)
    token, _ = Token.objects.get_or_create(user=admin)
    print(f"Admin user already exists: {admin_username}")
    print(f"Token: {token.key}")