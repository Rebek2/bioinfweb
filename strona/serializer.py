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



class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id','tagi']


class PostSerializer(serializers.ModelSerializer):
    tag = TagsSerializer(many = True)
    photos = MultimediaSerializer(many=True)
    class Meta:
        model = Post
        fields = ['id','title','content','author','date_created','tag','publish','event','photos']




class MembersSerializer(serializers.HyperlinkedModelSerializer):
    member_photo = MultimediaSerializer(many=True)
    class Meta:
        model = Members
        fields = ['id', 'user', 'position', 'about','email','member_photo']


