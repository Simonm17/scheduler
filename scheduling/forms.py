from django.forms import ModelForm
from django import forms
from .models import Appointment


class AppointmentForm(ModelForm):
    appointment_date = forms.DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local'
            },
            format='%Y-%m-%dT%H:%M'
        )
    )

    class Meta:
        model = Appointment
        fields = ['appointment_date']
