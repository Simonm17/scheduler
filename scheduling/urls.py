from django.urls import path
from .views import home


app_name = 'scheduling'

urlpatterns = [
    path('', home, name='home'),
]