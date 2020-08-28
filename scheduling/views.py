from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Appointment
from .forms import NewAppointmentForm
from applicants.models import Applicant
from applicants.forms import NewApplicantForm
from doctors.models import Doctor
from doctors.forms import NewDoctorForm


class AppointmentListView(LoginRequiredMixin, ListView):
    """
    TODO:   Current queryset displays all appts created by user.
            We need to have some more filters 
            to separate past and upcoming appts.
            Maybe within template conditions?
    """
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

@login_required
def schedule(request):
    if request.method == 'POST':
        applicant_form = NewApplicantForm(request.POST, prefix='a_form')
        doctor_form = NewDoctorForm(request.POST, prefix='d_form')
        scheduling_form = NewAppointmentForm(request.POST, prefix='s_form')
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
        applicant_form = NewApplicantForm(prefix='a_form')
        doctor_form = NewDoctorForm(prefix='d_form')
        scheduling_form = NewAppointmentForm(prefix='s_form')
    return render(request, 'scheduling/new_appointment.html', context={
        'a_form': applicant_form,
        'd_form': doctor_form,
        's_form': scheduling_form
        }
    )