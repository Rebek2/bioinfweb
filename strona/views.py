from django.shortcuts import render
from .models import Post,Comment,Galery,Tags
from .serializer import PostSerializer
from rest_framework import viewsets
# Create your views here.


def home(request):
    return render(request,'Home.html')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

