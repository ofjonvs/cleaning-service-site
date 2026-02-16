from django.shortcuts import render
from .models import Gallery, Review
# Create your views here.

def home(request):
    return render(request, "home/home.html", {'gallery_images': Gallery.objects.all()[:3], 'reviews': Review.objects.all()[:3]})

def gallery(request):
    return render(request, 'home/gallery.html', {'gallery_images': Gallery.objects.all()})

def reviews(request):
    return render(request, 'home/reviews.html', {'reviews': Review.objects.all()})

def booking(request):
    return render(request, 'home/booking.html')