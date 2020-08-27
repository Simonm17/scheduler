from django.urls import path
from .views import AppointmentListView


app_name = 'scheduling'

urlpatterns = [
    path('', AppointmentListView.as_view(), name='home'),
]