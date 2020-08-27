from django.urls import path
from .views import (
    AppointmentListView,
    AppointmentDetailView,
)


app_name = 'scheduling'

urlpatterns = [
    path('', AppointmentListView.as_view(), name='home'),
    path('appointment/<int:pk>/', AppointmentDetailView.as_view(), name='appointment'),
]