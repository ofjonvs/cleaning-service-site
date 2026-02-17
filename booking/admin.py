from django.contrib import admin
from .models import Appointment, Availability
from django import forms
# Register your models here.

class AppointmentAdminForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"
        widgets = {
            'appointment_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
        }

class AvailabilityAdminForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = "__all__"
        widgets = {
            'start_time': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            ),
            'end_time': forms.TimeInput(
                format='%H:%M',
                attrs={'type': 'time'}
            ),
        }

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    form = AvailabilityAdminForm

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentAdminForm