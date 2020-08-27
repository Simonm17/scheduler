from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Appointment


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'scheduling/home.html'
