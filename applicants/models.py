from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    """ Base abstract model for creating Applicant and Doctor models """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Applicant(Person):
    pass