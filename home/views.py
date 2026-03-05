from django.shortcuts import render, get_object_or_404
from .models import Gallery, Review, Product
from booking.models import Appointment
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
import stripe
# Create your views here.

def home(request):
    try:
        gallery_images = Gallery.objects.all()[:3]
        reviews = Review.objects.all()[:3]
        products = Product.objects.all()
    except Exception:
        gallery_images = []
        reviews = []

    for product in products:
        product.price = getStripePrice(product)
    return render(
        request,
        "home/home.html",
        {
            "gallery_images": gallery_images,
            "reviews": reviews,
            "products": products
        },
    )

def gallery(request):
    return render(request, 'home/gallery.html', {'gallery_images': Gallery.objects.all()})

def reviews(request):
    return render(request, 'home/reviews.html', {'reviews': Review.objects.all()})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    stripe_price = None
    if product.stripe_price_id:
        try:
            stripe_price = stripe.Price.retrieve(product.stripe_price_id)
            product_price = stripe_price.unit_amount / 100
        except stripe.error.StripeError:
            product_price = product.price
    else:
        product_price = product.price
    
    context = {
        'product': product,
        'price': product_price,
        'images': product.images.all(),
    }
    return render(request, 'home/product_detail.html', context)

@user_passes_test(lambda u: u.is_superuser)
def appointment_list(request):
    appointments = Appointment.objects.filter(
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')

    return render(request, 'home/appointments.html', {'appointments': appointments})

@user_passes_test(lambda u: u.is_superuser)
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    stripe_details = None
    if appointment.stripe_payment_intent_id:
        try:
            stripe_details = stripe.PaymentIntent.retrieve(appointment.stripe_payment_intent_id)
        except stripe.error.StripeError:
            pass
    
    context = {
        'appointment': appointment,
        'stripe_details': stripe_details,
    }
    return render(request, 'home/appointment_detail.html', context)

def getStripePrice(product):
    stripe_price = None
    if product.stripe_price_id:
        try:
            stripe_price = stripe.Price.retrieve(product.stripe_price_id)
            product_price = stripe_price.unit_amount / 100
        except stripe.error.StripeError:
            product_price = product.price
    else:
        product_price = product.price
    return product_price