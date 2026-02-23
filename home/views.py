from django.shortcuts import render
from .models import Gallery, Review
from booking.models import Appointment
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

def home(request):
    try:
        gallery_images = Gallery.objects.all()[:3]
        reviews = Review.objects.all()[:3]
    except Exception:
        gallery_images = []
        reviews = []

    return render(
        request,
        "home/home.html",
        {
            "gallery_images": gallery_images,
            "reviews": reviews,
        },
    )

def gallery(request):
    return render(request, 'home/gallery.html', {'gallery_images': Gallery.objects.all()})

def reviews(request):
    return render(request, 'home/reviews.html', {'reviews': Review.objects.all()})


@user_passes_test(lambda u: u.is_superuser)
def appointment_list(request):
    appointments = Appointment.objects.filter(
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')

    return render(request, 'home/appointments.html', {'appointments': appointments})