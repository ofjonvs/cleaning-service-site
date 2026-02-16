from django.shortcuts import render, redirect
import datetime
from .forms import AppointmentForm
from django.contrib import messages
import stripe
from .models import Appointment
from django.conf import settings

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
                return redirect('stripe_payment')
            else:
                # Mark as payment skipped
                appointment.payment_status = 'skipped'
                appointment.status = 'confirmed'
                appointment.save()
                messages.success(request, f'✓ Appointment booked successfully! We will confirm via email shortly.')
                # return redirect('booking_confirmation', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    
    # Get min and max dates (allow bookings 7 days in advance)
    min_date = datetime.datetime.now().date()
    max_date = min_date + datetime.timedelta(days=7)
    
    context = {
        'form': form,
        'min_date': min_date.isoformat(),
        'max_date': max_date.isoformat(),
    }
    return render(request, 'booking/booking.html', context)


def stripe_payment(request):
    """Stripe payment page"""
    try:
        appointment_id = request.session.get('appointment_id')
        appointment = Appointment.objects.get(id=appointment_id)
        
        if request.method == 'POST':
            try:
                # Create payment intent
                intent = stripe.PaymentIntent.create(
                    amount=int(appointment.amount * 100),  # Convert to cents
                    currency='usd',
                    metadata={
                        'appointment_id': appointment.id,
                        'customer_email': appointment.email,
                    }
                )
                
                appointment.stripe_payment_intent_id = intent.id
                appointment.payment_status = 'pending'
                appointment.save()
                
                context = {
                    'appointment': appointment,
                    'client_secret': intent.client_secret,
                    'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                    'amount': appointment.amount,
                }
                return render(request, 'booking/stripe_payment.html', context)
            except stripe.error.StripeError as e:
                messages.error(request, f'Payment error: {str(e)}')
                return redirect('booking')
        
        context = {
            'appointment': appointment,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, 'booking/stripe_payment.html', context)
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found.')
        return redirect('booking')
    