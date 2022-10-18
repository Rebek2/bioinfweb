from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField
from datetime import date
# Create your models here.
import datetime

class Post(models.Model):
    title = models.CharField(max_length = 30)
    content = models.TextField(max_length = 10000)
    author = models.CharField(max_length = 10)
    date_created = models.DateTimeField(auto_now_add = True)
    tag = models.ManyToManyField('Tags', blank = True, null = True)
    publish = models.BooleanField(default = True)
    event = models.BooleanField(default = False)
    views = models.BigIntegerField(default = 0)
    facebook_id = models.TextField( max_length=250)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title

    def get_time_display(self):
        return(f'{self.date_created.strftime("%Y-%m-%d  %H:%M:%S")}')

    def get_absolute_url(self):
        return(f'{self.title.replace(" ","-")}-{self.date_created.strftime("%Y-%m-%d")}')

    def add_view(self):
        self.views = self.views + 1

class Comment(models.Model):
    content = models.TextField(max_length=1000)
    User = models.CharField(max_length=10)#to bedzie po prostu do wpisania przez uzytkownika bez potrzeby logowania.
    post = models.ForeignKey(Post,
                             null=True,
                             blank=True,
                             on_delete=models.SET_NULL,
                             related_name='comments')

    date = models.DateTimeField(auto_now_add = True)

    def get_time(self):
        return(f'{self.date.strftime("%Y-%m-%d %H:%M:%S")}')

    class Meta:
        ordering = ['-date']
    #
    # def when(self):
    #     when = datetime.datetime.now() - self.date
    #     return (f'{when.strftime("%Y/%m/%d  Godzina:%H:%M:%S")}')

    def __str__(self):
        return self.User


class Multimedia(models.Model):

    post = models.ForeignKey(Post,
                              on_delete=models.CASCADE,
                              related_name ='photos',
                              blank=True,
                              null=True)

    members = models.ForeignKey('Members',
                                on_delete=models.CASCADE,
                                related_name='member_photo',
                                blank=True,
                                null=True)

    photos = VersatileImageField(
        'Image',
        upload_to='photos/',
        ppoi_field='image_ppoi',
        blank=True,
        null=True
    )
    image_ppoi = PPOIField()
    gallery = models.ForeignKey('Galery',
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                related_name ='gallery_photos' )


class Tags(models.Model):
    tagi = models.CharField(max_length= 30)

    def __str__(self):
        return self.tagi


class Galery(models.Model):
    OpisGalerii = models.CharField(max_length = 40)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.OpisGalerii


class Members(models.Model):
    user = models.CharField(max_length=120)
    position = models.CharField(max_length=150)
    about = models.CharField(max_length=1000)
    email = models.CharField(max_length = 100, default='none')

    def __str__(self):
        return self.user


class Registration(models.Model):
    nick = models.CharField(max_length=120, blank=True, null=True)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    number = models.CharField(max_length=12)
    wydzial = models.CharField(max_length=300)
    kierunek = models.CharField(max_length=300)
    rok = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.surname

    def get_time(self):
        return(f'{self.date.strftime("%Y-%m-%d %H:%M:%S")}')


