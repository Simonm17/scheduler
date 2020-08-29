from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('scheduling.urls', namespace='scheduling')),
    path('applicants/', include('applicants.urls', namespace='applicants')),
    path('doctors/', include('doctors.urls', namespace='doctors')),
]
