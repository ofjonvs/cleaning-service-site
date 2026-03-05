from django.shortcuts import get_object_or_404, render, redirect
import datetime
from .forms import AppointmentForm
from django.contrib import messages
import stripe
from .models import Appointment, Availability
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_GET


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def booking(request):
    """Main booking page"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            
            # Store appointment ID in session for payment
            request.session['appointment_id'] = appointment.id
            
            # Check if user wants to pay or skip
            payment_option = request.POST.get('payment_option', 'skip')
            
            if payment_option == 'pay':
                request.session['appointment_id'] = appointment.id
                return redirect('checkout', appointment_id=appointment.id)
            else:
                # Mark as payment skipped
                appointment.payment_status = 'skipped'
                appointment.status = 'pending'
                appointment.save()
                messages.warning(request, f'Appointment Pending')
                return redirect('confirmation', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    
    # Get min and max dates (allow bookings 7 days in advance)
    min_date = datetime.datetime.now().date() + datetime.timedelta(days=1)
    max_date = min_date + datetime.timedelta(days=7)
    
    context = {
        'form': form,
        'min_date': min_date.isoformat(),
        'max_date': max_date.isoformat(),
    }
    return render(request, 'booking/booking.html', context)


def stripe_checkout(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    session = stripe.checkout.Session.create(
        mode='payment',
        payment_method_types=['card'],
        line_items=[{
            'price': appointment.product.stripe_price_id,
            'quantity': 1,
        }],
        success_url=request.build_absolute_uri(
            reverse('success', args=[appointment.id])
        ),
        cancel_url=request.build_absolute_uri(reverse('confirmation', args=[appointment.id])),
        metadata={
            'appointment_id': appointment.id,
        }
    )

    appointment.stripe_session_id = session.id
    appointment.payment_status = 'cancelled'
    appointment.save()

    return redirect(session.url)

def payment_success(request, appointment_id):
    """Handle successful Stripe payment"""
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        if appointment.payment_status == 'pending':
            appointment.payment_status = 'paid'
            appointment.status = 'confirmed'
            appointment.save()
            
            messages.success(request, '✓ Payment successful! Your appointment is confirmed.')
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found.')
    
    return redirect('confirmation', appointment_id=appointment_id)


def booking_confirmation(request, appointment_id):
    """Display booking confirmation"""
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if appointment.payment_status == 'cancelled':
            appointment.delete()
            return render(request, 'booking/booking_cancellation.html')
        return render(request, 'booking/booking_confirmation.html', {'appointment': appointment})
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found.')
        return redirect('booking')
    
@require_GET
def get_available_slots(request):
    """AJAX endpoint to get available slots for a given date"""

    if not (date_str:=request.GET.get('date')):
        return JsonResponse({'slots': []})
    
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

        availabilities = Availability.objects.filter(
            day_of_week=date.weekday(),
            is_active=True
        )
        
        slots = []
        for availability in availabilities:
            start = datetime.datetime.combine(date, availability.start_time)
            end = datetime.datetime.combine(date, availability.end_time)
            current = start
            
            while current < end:
                if not Appointment.objects.filter(appointment_date=current, status__in=['confirmed', 'completed']).exists():
                    slots.append({
                        'time': current.strftime('%I:%M %p').lstrip('0'),
                        'datetime': current.isoformat()
                    })
                    current += datetime.timedelta(minutes=30)    
                else:
                    for _ in (range(min(len(slots), 3))):
                        slots.pop()
                    current += datetime.timedelta(minutes=60)
        
        return JsonResponse({'slots': slots})
    except:
        return JsonResponse({'slots': []})