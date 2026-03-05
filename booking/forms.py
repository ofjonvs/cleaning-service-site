from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import Appointment
from datetime import datetime, timedelta
from home.models import Product

class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'hidden': True
        }),
        label='Select Date & Time'
    )

    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True),
        empty_label="Select a service",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Service"
    )
    
    class Meta:
        model = Appointment
        fields = ['name', 'phone', 'appointment_date', 'product', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Additional notes or special requests (optional)'
            }),
        }