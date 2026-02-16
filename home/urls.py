from django.urls import path
from .views import home, gallery, reviews

urlpatterns = [
    path("", home, name="home"),
    path('gallery', gallery, name='gallery'),
    path('reviews', reviews, name='reviews'),
]