from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.timezone import now


class UserProf(models.Model):
    image = models.ImageField(upload_to="profiles/",default="profiles/profile.png")
    username = models.CharField(max_length=20,default=None)
    email = models.EmailField()
    password = models.CharField(max_length=32,default=None)
    address = models.CharField(max_length=99,default=None)
    city = models.CharField(max_length=20,default=None)
    phone = models.CharField('phone', max_length=10, validators=[MinLengthValidator(10)],default=None)
    state = models.CharField(max_length=20,default=None)

    class Meta:
        db_table = "user_details"