from django.shortcuts import render
from .serializer import *
from rest_framework import viewsets
from .DAL import Database
# Create your views here.


def home(request):
    print('czesc')
    a = Database()
    print(a.retrieve_posts_by_date("2022-04-28"))
    #print(a.retrieve_post_by_title("Testowy"))
    #a.modify_tag_name_by_id(3,"zmienionyTag")
    #a.add_tag('#dodanyprzezApi')
    #print(a.retrieve_tag(1))
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
