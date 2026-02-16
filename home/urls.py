from django.contrib import admin
from django.urls import path, include
from .views import home, gallery, reviews, booking

urlpatterns = [
    path("", home, name="home"),
    path('gallery', gallery, name='gallery'),
    path('reviews', reviews, name='reviews'),
    # path('booking', booking, name='booking')
]