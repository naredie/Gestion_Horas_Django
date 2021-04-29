from typing import Optional, Sequence

from django.contrib.auth import get_user_model

from horas.apps.accounts.enums import UserRole
from horas.apps.accounts.models import Tenant

User = get_user_model()


def create_user(username: str, roles: Optional[Sequence[UserRole]] = None):
    """
    Create user helper funtion.

    Important: Only use it for testing.
    """
    roles = roles or []
    is_employee = is_manager = is_human_resources = False
    for role in roles:
        if role == UserRole.EMPLOYEE:
            is_employee = True
        elif role == UserRole.MANAGER:
            is_manager = True
        elif role == UserRole.HUMAN_RESOURCES:
            is_human_resources = True
        else:
            raise NotImplementedError

    tenant = Tenant(name="tenant" + username)
    tenant.save()
    user = User.objects.create_user(
        username=username,
        password="12test12",
        email="test@example.com",
        tenant=tenant,
        is_user=is_employee,
        is_manager=is_manager,
        is_human_resources=is_human_resources,
    )
    user.save()
    return user
