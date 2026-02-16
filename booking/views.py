from django.shortcuts import render, redirect
import datetime
from .forms import AppointmentForm
from django.contrib import messages

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
