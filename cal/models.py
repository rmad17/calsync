from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Events(models.Model):
    user = models.ForeignKey(User)
    description = models.CharField(max_length=500, unique=True)
    updated = models.DateTimeField(auto_now=False, auto_now_add=False)
