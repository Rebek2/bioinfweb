from django.db import models
#from django.contrib.auth.models import User


class Tags(models.Model):
    title = models.CharField(max_length=100, default="")


class Multimedia(models.Model):
    picture = models.ImageField()


class Comment(models.Model):
    content = models.TextField(max_length=300, default="")
    #user = models.ForeignKey(to=User, on_delete=models.CASCADE, default="")
    date = models.DateField()


class Post(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(default="")
    content = models.TextField(max_length=300)
    #added_by = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, default="")
    tags = models.ManyToManyField(Tags)
    multimedia = models.OneToOneField(Multimedia, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.title

# Create your models here.
# Create your models here.
