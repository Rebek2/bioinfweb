from django.shortcuts import render
from .serializer import *
from rest_framework import viewsets
from .DAL import Database
# Create your views here.
from rest_framework import generics

def home(request):
    print('czesc')
    #a = Database()
    #a.add_new_post("Test3","Nowości w postach teraz się dzieją","Arjin")
    #a.change_tags_in_post('#innytag',1)
    #print(a.retrive_mutlimedia())
    #print(a.retrive_posts_values())
    return render(request, 'Home.html')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class MultimediaViewSet(viewsets.ModelViewSet):
    queryset = Multimedia.objects.all()
    serializer_class = MultimediaSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


