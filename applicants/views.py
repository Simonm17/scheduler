from django.shortcuts import render
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Applicant
from .forms import ApplicantForm

class ApplicantUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Applicant
    form_class = ApplicantForm
    template_name = 'applicants/update_applicant.html'
    success_message = 'You have successfully updated the contact.'

    def test_func(self):
        """ Validate whether user is staff or scheduler. """
        appointment = self.get_object()
        user = self.request.user
        if user.is_staff or user == appointment.created_by:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_url'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url