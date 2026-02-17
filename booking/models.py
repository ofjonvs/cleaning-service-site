from django.db import models
from django.contrib.auth.models import User

class Availability(models.Model):
    """Stores available time slots for bookings"""
    day_of_week = models.IntegerField(
        choices=[
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday'),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('day_of_week', 'start_time', 'end_time')
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        day_name = dict(self._meta.get_field('day_of_week').choices).get(self.day_of_week)
        return f"{day_name}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


class Appointment(models.Model):
    """Stores customer bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('pending', 'Payment Pending'),
        ('paid', 'Paid'),
        ('skipped', 'Payment Skipped'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    appointment_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['appointment_date']
    
    def __str__(self):
        return f"{self.name} - {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"