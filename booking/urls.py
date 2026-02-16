from django.urls import path
from . import views
from .views import booking

urlpatterns = [
    path("", booking, name="booking"),
]