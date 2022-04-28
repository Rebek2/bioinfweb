from .models import Post,Comment,Tags,Galery,Multimedia
from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer




class MultimediaSerializer(serializers.HyperlinkedModelSerializer):
    photos = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
        ]
    )

    class Meta:
        model = Multimedia
        fields = ['photos']

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','content','User','post','date']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    comments = CommentSerializer(many=True)
    photos = MultimediaSerializer(many = True)
    class Meta:
        model = Post
        fields = ['id','title','content','author','date_created','tag','publish','comments','photos']



class MultimediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Multimedia
        fields = ['id','post','photos']


class TagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ['id','tagi']