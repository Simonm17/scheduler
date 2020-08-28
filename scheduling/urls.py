from django.urls import path
from .views import (
    AppointmentListView,
    AppointmentDetailView,
    schedule,
)


app_name = 'scheduling'

urlpatterns = [
    path('', AppointmentListView.as_view(), name='home'),
    path('appointment/new/', schedule, name='new_appointment'),
    path('appointment/<int:pk>/', AppointmentDetailView.as_view(), name='appointment'),
]