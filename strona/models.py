from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField
# Create your models here.
class Post(models.Model):

    title = models.CharField(max_length = 30)
    content = models.TextField(max_length = 10000)
    author = models.CharField(max_length = 10)
    date_created = models.DateTimeField(auto_now_add = True)
    tag = models.ManyToManyField('Tags',blank = True)
    publish = models.BooleanField(default = False)

    class Meta:
        ordering = ('-date_created',)
    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(max_length = 1000)
    User = models.CharField(max_length = 10)#to bedzie po prostu do wpisania przez uzytkownika bez potrzeby logowania.
    post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name = 'comments')
    date = models.DateTimeField(auto_now_add = True)
    class Meta:
        ordering = ['-date']
    def __str__(self):
        return self.User


class Multimedia(models.Model):
<<<<<<< HEAD

    post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name = 'photos',blank = True) #bedzie mozna dodawac kilka zdjec do jednego posta.
    photos = VersatileImageField(
        'Image',
        upload_to='photos/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()
=======
    title = models.CharField(max_length=250)
    photos = models.ImageField(upload_to='photos/')
    post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name = 'photos',blank = True) #bedzie mozna dodawac kilka zdjec do jednego posta.
    def __str__(self):
        return self.title
>>>>>>> main

class Tags(models.Model):
    tagi = models.CharField(max_length = 30)


    def __str__(self):
        return self.tagi


class Galery(models.Model):

    OpisGalerii = models.CharField(max_length = 40)

    def __str__(self):
        return self.OpisGalerii