from django.forms import forms, ModelForm, TextInput

from .models import Applicant


class NewApplicantForm(ModelForm):

    class Meta:
        model = Applicant
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': 'Applicant first name',
            'last_name': 'Applicant last name',
        }