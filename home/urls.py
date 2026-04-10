from django.http import HttpResponse
from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path('gallery', gallery, name='gallery'),
    path('reviews', reviews, name='reviews'),
    path('appointments', appointment_list, name='appointments'),
    path('product/<int:service_id>/', product_detail, name='product_detail'),
    path('appointment/<int:appointment_id>/', appointment_detail, name='appointment_detail'),
    path('health/', lambda x: HttpResponse("OK"), name='health'),
    path('heartbeat/', lambda x: HttpResponse("Heartbeat"), name='heartbeat'),
]