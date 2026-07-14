from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord')
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='tenant'
    )


    def __str__(self):
        return self.get_full_name() or self.username


    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
