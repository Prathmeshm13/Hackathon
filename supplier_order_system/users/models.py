from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_supplier = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    # Add related_name to prevent clashes with default User model
    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_groups', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_user_permissions', blank=True
    )
