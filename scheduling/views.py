from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Appointment


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'scheduling/home.html'

    def get_queryset(self):
        """ 
        Return list of appointments scheduled by currently logged in user. 
        """
        user = self.request.user
        queryset = Appointment.objects.filter(created_by=user)
        queryset = queryset.order_by('appointment_date')
        return queryset


