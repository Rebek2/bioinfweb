from .models import Post,Comment,Tags,Galery,Multimedia
from rest_framework import serializers



class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','content','User','post','date']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    comments = CommentSerializer(many=True)
    class Meta:
        model = Post
        fields = ['id','title','content','author','date_created','tag','publish','comments']

class MultimediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Multimedia
        fields = ['id','post','photos']


class TagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ['id','tagi']

