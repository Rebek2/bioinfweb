from django.contrib import admin
from .models import Post, Comment, Multimedia

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Multimedia)


# Register your models here.
