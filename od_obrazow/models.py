from django.db import models
from django.utils import timezone

class MultiMedia(models.Model):
    title = models.CharField(max_length=250)
    when = models.DateTimeField('added', default=timezone.now())
    image = models.ImageField(upload_to='image/')

    def __str__(self):
        return self.title

# Create your models here.