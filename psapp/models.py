from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError



def property_image_path(instance, filename):
    return f'properties/{instance.property.id}/{filename}'



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



class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio')
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='properties'
    )

    title = models.CharField(max_length=100)
    description = models.TextField()

    location = models.CharField(max_length=200)
    price_per_month = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    room_count = models.PositiveIntegerField()

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.title}: {self.price_per_month}'


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



class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    start_date = models.DateField()
    end_date = models.DateField()

    booking_date = models.DateTimeField(auto_now_add=True)

    cancellation_deadline = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                'End date must be after start date'
            )


    def __str__(self):
        return f'{self.tenant} - {self.property}'


    class Meta:
        ordering = ['-booking_date']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'



class Review(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Rating {self.rating} for {self.property}'


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
