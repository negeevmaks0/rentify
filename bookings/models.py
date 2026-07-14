from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator

from users.models import User
from properties.models import Property



def validate_future_date(value):
    if value <= timezone.now().date():
        raise ValidationError(
            'Booking date must be in the future'
        )


# Create your models here.

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.PROTECT,
        related_name='bookings'
    )

    tenant = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='bookings'
    )

    start_date = models.DateField(validators=[validate_future_date])
    end_date = models.DateField()

    booking_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0)
        ],
        default=0
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    cancellation_deadline = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f'{self.tenant} - {self.property}'


    class Meta:
        ordering = ['-booking_date']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    end_date__gte=models.F('start_date')
                ),
                name='booking_end_after_start'
            )
        ]
