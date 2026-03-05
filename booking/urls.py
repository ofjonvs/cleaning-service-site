from django.urls import path
from .views import *

urlpatterns = [
    path("", booking, name="booking"),
    path('checkout/<int:appointment_id>/', stripe_checkout, name='checkout'),
    path('success/<int:appointment_id>/', payment_success, name='success'),
    path('failure/<int:appointment_id>/', payment_failure, name='failure'),
    path('confirmation/<int:appointment_id>/', booking_confirmation, name='confirmation'),
    path('get-available-slots', get_available_slots, name='get_available_slots')
]