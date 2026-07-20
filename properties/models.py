from django.db import models
from users.models import User

from django.core.validators import MinValueValidator

# Create your models here.

def property_image_path(instance, filename):
    return f'properties/{instance.property.id}/{filename}'


class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio')
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='properties'
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )

    room_count = models.PositiveIntegerField()

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.title}: {self.price_per_night}/night'


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to=property_image_path)


    def __str__(self):
        return f'Image for {self.property.title}'


    class Meta:
        ordering = ['id']
        verbose_name = 'Property image'
        verbose_name_plural = 'Property images'