from django.http import HttpResponse
from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path('gallery', gallery, name='gallery'),
    path('reviews', reviews, name='reviews'),
    path('appointments', appointment_list, name='appointments'),
    path('health/', lambda x: HttpResponse("OK"), name='health')
]