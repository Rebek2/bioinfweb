from .models import Post, Comment, Tags, Multimedia, Members,Galery
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
        fields = ['id','content','User','post','date','get_time']



class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id','tagi']


class PostSerializer(serializers.ModelSerializer):
    tag = TagsSerializer(many = True)
    photos = MultimediaSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id','title','content',
                  'author','date_created','tag',
                  'publish','event','photos',
                  'get_absolute_url','get_time_display']




class MembersSerializer(serializers.HyperlinkedModelSerializer):
    member_photo = MultimediaSerializer(many=True)
    class Meta:
        model = Members
        fields = ['id', 'user', 'position', 'about','email','member_photo']


class GallerySerializer(serializers.HyperlinkedModelSerializer):
    gallery_photos = MultimediaSerializer(many = True)
    class Meta:
        model = Galery
        fields = ['OpisGalerii','gallery_photos','date']