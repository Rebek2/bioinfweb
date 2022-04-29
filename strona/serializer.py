from .models import Post, Comment, Tags, Galery, Multimedia
from rest_framework import serializers


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content','author', 'date_created', 'tag', 'publish']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','content','User','post','date']


class MultimediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Multimedia
        fields = ['id','post','photos', 'title']


class TagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ['id','tagi']

class GalerySerialiazer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Galery
        fields = ['OpisGalerii']