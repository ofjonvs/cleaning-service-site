from django.db import models

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

    
class Product(models.Model):
    """Service products for booking (e.g., Basic Clean, Deep Clean)"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField(help_text="Estimated duration in minutes")
    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Stripe price ID (e.g., price_1234...)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.name

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Review,
        related_name='images',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    product = models.ForeignKey(
        Product,
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