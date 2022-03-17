from django.db import models
from django.contrib.auth.models import User



class Post(models.Model):
    media = models.CharField(max_length=100)


# Create your models here.
