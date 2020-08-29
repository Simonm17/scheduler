from datetime import date

from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, 
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Appointment
from .forms import AppointmentForm
from applicants.models import Applicant
from applicants.forms import ApplicantForm
from doctors.models import Doctor
from doctors.forms import DoctorForm


class AppointmentListView(LoginRequiredMixin, ListView):

    model = Appointment
    template_name = 'scheduling/home.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        today = date.today()
        context = super().get_context_data(**kwargs)
        context['timezone_now'] = timezone.now()
        context['todays_appointments'] = Appointment.objects.filter(
            created_by=user,
            appointment_date__year=today.year,
            appointment_date__month=today.month,
            appointment_date__day=today.day,
        ).order_by('appointment_date')
        context['upcoming_appointments'] = Appointment.objects.filter(
            created_by=user,
            appointment_date__date__gt=today
        ).order_by('appointment_date')
        context['past_appointments'] = Appointment.objects.filter(
            created_by=user, 
            appointment_date__date__lt=today 
        ).order_by('-appointment_date')
        return context


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


@login_required
def schedule(request):
    if request.method == 'POST':
        applicant_form = ApplicantForm(request.POST, prefix='a_form')
        doctor_form = DoctorForm(request.POST, prefix='d_form')
        scheduling_form = AppointmentForm(request.POST, prefix='s_form')
        if applicant_form.is_valid() and doctor_form.is_valid() and scheduling_form.is_valid():
            # save applicant object
            applicant = applicant_form.save(commit=False)
            applicant.created_by = request.user
            applicant.save()
            # save doctor object
            doctor = doctor_form.save(commit=False)
            doctor.created_by = request.user
            doctor.save()
            # save appointment object with app/doc instance
            appointment = scheduling_form.save(commit=False)
            appointment.applicant = applicant
            appointment.doctor = doctor
            appointment.created_by = request.user
            appointment.save()
            messages.success(request, f'Your appointment is scheduled.')
            # redirect user to appointment object's detailview
            return redirect('scheduling:appointment', appointment.pk)
    else:
        applicant_form = ApplicantForm(prefix='a_form')
        doctor_form = DoctorForm(prefix='d_form')
        scheduling_form = AppointmentForm(prefix='s_form')
    return render(request, 'scheduling/new_appointment.html', context={
        'a_form': applicant_form,
        'd_form': doctor_form,
        's_form': scheduling_form
        }
    )


class AppointmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'scheduling/update_appointment.html'

    def test_func(self):
        """ Validate whether user is staff or scheduler. """
        appointment = self.get_object()
        user = self.request.user
        if user.is_staff or user == appointment.created_by:
            return True
        return False

class AppointmentDeleteview(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('scheduling:home')

    def test_func(self):
        """ Validate whether user is staff or scheduler. """
        appointment = self.get_object()
        user = self.request.user
        if user.is_staff or user == appointment.created_by:
            return True
        return False