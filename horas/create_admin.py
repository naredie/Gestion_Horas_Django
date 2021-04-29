"""
Script to create admin user within a dummy tenant. Only for development.
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horas.settings")
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Tenant

User = get_user_model()
tenant = Tenant(name="admin_tenant")
tenant.save()
User.objects.create_superuser(
    username='admin',
    email='admin@myproject.com',
    password='admin',
    tenant=tenant,
    is_user=True,
    is_manager=True,
    is_human_resources=True,
).save()
