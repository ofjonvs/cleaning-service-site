from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
    
class Review(models.Model):
    author = models.CharField(max_length=100)
    text = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=5, choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author} - {self.rating}★"

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='products')
    size = models.CharField(max_length=10, choices=[(s, s.capitalize()) for s in ('small', 'medium', 'large')], default='small')
    duration_minutes = models.IntegerField(help_text="Estimated duration in minutes")
    stripe_price_id = models.CharField(
        max_length=255,
        help_text="Stripe price ID (e.g., price_1234...)"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.service.name + ' - ' + self.size
    
class AddOns(models.Model):
    name = models.CharField(max_length=30)
    stripe_price_id = models.CharField(
        max_length=255,
        help_text="Stripe price ID (e.g., price_1234...)"
    )
    price = models.DecimalField(decimal_places=2, max_digits=5, help_text="Add on cost", blank=True, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name + ' - ' + str(self.price)
    
    def save(self, *args, **kwargs):
        from .utils import getStripePrice
        self.price = getStripePrice(self.stripe_price_id)
        super(AddOns, self).save(*args, **kwargs)

class Gallery(models.Model):
    image = CloudinaryField('image', folder='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Review,
        related_name='images',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    service = models.ForeignKey(
        Service,
        related_name='images',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = "Gallery"
    
    def __str__(self):
        return f'image {self.pk}'