from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=50, blank=False)

    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Custom User model"""

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, blank=False)
    office_city = models.CharField(max_length=50, blank=True, null=True)
    weekly_hours = models.FloatField(max_length=10, default=38.5)
    is_human_resources = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message=(
            "El formato de telefono tiene que ser '+34655555444'. "
            "Se permite hasta 15 digitos."
        ),
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    REQUIRED_FIELDS = ["tenant"]

    def get_user_city(self):
        return self.office_city

    def get_user_weekly_hours(self):
        return self.weekly_hours

    def get_user_manager(self):
        return self.manager
