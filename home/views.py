from django.shortcuts import render, get_object_or_404
from .models import Gallery, Review, Product, Service
from booking.models import Appointment
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
import stripe
from .utils import *

# Create your views here.

def home(request):
    try:
        gallery_images = Gallery.objects.all()[:3]
        reviews = Review.objects.all()[:3]
        services = Service.objects.all()
    except Exception:
        gallery_images = []
        reviews = []

    for service in services:
        setServicePrices(service)
    return render(
        request,
        "home/home.html",
        {
            "gallery_images": gallery_images,
            "reviews": reviews,
            "services": services
        },
    )

def gallery(request):
    return render(request, 'home/gallery.html', {'gallery_images': Gallery.objects.all()})

def reviews(request):
    return render(request, 'home/reviews.html', {'reviews': Review.objects.all()})

def product_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id, is_active=True)
    setServicePrices(service)
    return render(request, 'home/product_detail.html', {
        'service': service,
        'images': service.images.all(),
    })

@user_passes_test(lambda u: u.is_superuser)
def appointment_list(request):
    appointments = Appointment.objects.filter(
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')
    for appointment in appointments:
        appointment.addons_str = ', '.join(addon.name for addon in appointment.addons.all())

    return render(request, 'home/appointments.html', {'appointments': appointments})

@user_passes_test(lambda u: u.is_superuser)
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.addons_str = ', '.join(addon.name for addon in appointment.addons.all())
    stripe_details = None
    if appointment.stripe_payment_intent_id:
        try:
            stripe_details = stripe.PaymentIntent.retrieve(appointment.stripe_payment_intent_id)
            stripe_details.amount /= 100
        except stripe.error.StripeError:
            pass
    context = {
        'appointment': appointment,
        'stripe_details': stripe_details,
    }
    return render(request, 'home/appointment_detail.html', context)
