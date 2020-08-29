from django.urls import path

from .views import DoctorUpdateView


app_name = 'doctors'

urlpatterns = [
    path('doctors/<int:pk>/update/', DoctorUpdateView.as_view(), name='update'),
]