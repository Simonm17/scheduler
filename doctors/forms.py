from django.forms import forms, ModelForm, TextInput

from .models import Doctor

class NewDoctorForm(ModelForm):

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': 'Doctor first name',
            'last_name': 'Doctor last name',
        }