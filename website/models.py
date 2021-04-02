from django.db import models
from django.utils.timezone import now

class Contact(models.Model):
    email = models.EmailField(max_length=50)
    name = models.CharField(max_length=50)
    message = models.TextField(max_length=500)
    time = models.DateTimeField(default=now)
 
