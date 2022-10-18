from .models import Post, Comment, Tags, Multimedia, Members, Galery, Registration
from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class MultimediaSerializer(serializers.ModelSerializer):
    photos = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
        ]
    )

    class Meta:
        model = Multimedia
        fields = ['id','photos','post','gallery']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','content','User','post','date','get_time']



class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id','tagi']


class PostSerializer(serializers.ModelSerializer):
    tag = TagsSerializer(many = True,required = False)
    photos = MultimediaSerializer(many=True,required = False)

    class Meta:
        model = Post
        fields = ['id','title','content',
                  'author','date_created','tag',
                  'publish','event','photos',
                  'get_absolute_url','get_time_display',
                  'views','facebook_id']




class MembersSerializer(serializers.HyperlinkedModelSerializer):
    member_photo = MultimediaSerializer(many=True,required = False)
    class Meta:
        model = Members
        fields = ['id', 'user', 'position', 'about','email','member_photo']

class GallerySerializer(serializers.HyperlinkedModelSerializer):
    gallery_photos = MultimediaSerializer(many = True,required = False)
    class Meta:
        model = Galery
        fields = ['id','OpisGalerii','gallery_photos','date']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ["nick", "name", "surname", "email", "number", "wydzial", "kierunek", "rok",'get_time']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user




