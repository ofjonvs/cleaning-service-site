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

class Gallery(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Review,
        related_name='images',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = "Gallery"
    
    def __str__(self):
        return self.title or f'image {self.pk}'