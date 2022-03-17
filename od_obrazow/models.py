from django.db import models

class MultiMedia(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='media/')
# Create your models here.
