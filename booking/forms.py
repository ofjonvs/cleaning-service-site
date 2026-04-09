from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import Appointment
from datetime import datetime, timedelta
from home.models import Service, AddOns

BEDROOM_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4+'),
]

BATHROOM_CHOICES = [
    (0.5, '0.5'),
    (1, '1'),
    (1.5, '1.5'),
    (2, '2'),
    (2.5, '2.5'),
    (3, '3+'),
]

OTHER_ROOM_CHOICES = [
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4+'),
]

class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'hidden': True
        }),
        label='Select Date & Time'
    )

    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        empty_label="Select a service",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Service"
    )

    addons = forms.ModelMultipleChoiceField(
        queryset=AddOns.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Add-Ons"
    )

    address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your address',
            'id': 'autocomplete'
        }),
        label="Address"
    )

    bedrooms = forms.ChoiceField(
        choices=BEDROOM_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'horizontal-radio'}),
        label="Bedrooms"
    )

    bathrooms = forms.ChoiceField(
        choices=BATHROOM_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'horizontal-radio'}),
        label="Bathrooms"
    )

    other_rooms = forms.ChoiceField(
        choices=OTHER_ROOM_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'horizontal-radio'}),
        label="Other Rooms"
    )

    class Meta:
        model = Appointment
        fields = ['name', 'phone', 'address', 'appointment_date', 'addons', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Additional notes or special requests (optional)'
            }),
        }