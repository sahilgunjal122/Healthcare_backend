
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    name = models.CharField(max_length=255)
    dob = models.DateField()
    contact = models.CharField(max_length=255)
    address = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    
    def __str__(self):
        return self.name