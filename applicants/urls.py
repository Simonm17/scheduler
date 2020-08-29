from django.urls import path

from .views import ApplicantUpdateView


app_name = 'applicants'

urlpatterns = [
    path('applicants/<int:pk>/update/', ApplicantUpdateView.as_view(), name='update'),
]