from django.shortcuts import render
from .models import Post,Comment,Galery,Tags,Multimedia
from .serializer import *
from rest_framework import viewsets
# Create your views here.
from rest_framework import generics

def home(request):
    return render(request,'Home.html')


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

<<<<<<< HEAD

=======
class PurchaseList(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        post = self.kwargs['post']
        return Comment.objects.filter(post_id=post).all()
>>>>>>> main
