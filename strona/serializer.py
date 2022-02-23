from .models import Post,Comment,Tags,Galery
from rest_framework import serializers

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','content','author','date_created','tag','publish']


