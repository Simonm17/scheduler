from datetime import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from applicants.models import Applicant
from doctors.models import Doctor


class AppointmentManager(models.Manager):

    def upcoming_appointments(self, **kwargs):
        return self.filter(appointment_date__gt=timezone.now())

    def todays_appointments(self, **kwargs):
        return self.filter(appointment_date=timezone.now().date())

    def past_appointments(self, **kwargs):
        return self.filter(appointment_date__lt=timezone.now())


class Appointment(models.Model):
    appointment_date = models.DateTimeField()
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    doctors = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.appointment_date}'

    objects = models.Manager()
    objects = AppointmentManager()

