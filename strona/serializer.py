from .models import Post, Comment, Tags, Multimedia, Members
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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','content','User','post','date']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    photos = MultimediaSerializer(many=True)
    class Meta:
        model = Post
        fields = ['id','title','content','author','date_created','tag','publish','photos']


class TagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ['id','tagi']


class MembersSerializer(serializers.HyperlinkedModelSerializer):
    member_photo = MultimediaSerializer(many=True)
    class Meta:
        model = Members
        fields = ['id', 'user', 'position', 'about', 'email']


