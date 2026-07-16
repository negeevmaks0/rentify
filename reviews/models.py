from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User
from bookings.models import Booking




# Create your models here.

class Review(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.PROTECT,
        related_name='review'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
        return f'{self.rating}/5 - Booking #{self.booking_id}'


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
