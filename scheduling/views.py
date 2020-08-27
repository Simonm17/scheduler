from django.shortcuts import render
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
)
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


class AppointmentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Appointment
    template_name = 'scheduling/appointment.html'

    def test_func(self):
        """ Validate whether user is staff or scheduler. """
        appointment = self.get_object()
        user = self.request.user
        if user.is_staff or user == appointment.created_by:
            return True
        return False