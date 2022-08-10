from django.shortcuts import render
from .serializer import *
from rest_framework import viewsets
from .DAL import Database
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from rest_framework.decorators import api_view, parser_classes,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

def home(request):
    print('czesc')
    a = Database()
    a.add_to_gallery(1,1)
    return render(request, 'Home.html')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Members.objects.all()
    serializer_class = MembersSerializer


class GaleryVievSet(viewsets.ModelViewSet):
    queryset = Galery.objects.all()
    serializer_class = GalerySerializer

class RegistrationVievSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


@api_view(['GET'])
def CommentsOfPost(request,id):
    comments = Comment.objects.all().filter(post_id = id)
    serializer = CommentSerializer(comments,many=True)
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes([JSONParser])
def UpdatePost(request, id):
    a = Database()
    choice_tags = request.data["tag_handling"]
    t = request.data["title"]
    c = request.data["content"]
    au = request.data["author"]
    tag_name = request.data["tag_name"]
    tag_id = int(request.data["tag_id"])

    if choice_tags == "":
        return Response(a.modify_post_by_id(id, t, c, au))

    elif choice_tags == "add_new":
        return Response(a.modify_post_by_id(id, t, c, au),
                        a.add_tag_to_post(tag_name, id))

    elif choice_tags == "add_existing":
        return Response(a.modify_post_by_id(id, t, c, au),
                        a.add_existing_tag_to_post(tag_id, id))

    elif choice_tags == "remove":
        return Response(a.modify_post_by_id(id, t, c, au),
                        a.remove_tag_from_post(id, tag_id))
    else:
        return Response("Possible tag handling command are: '', add_new, add_existing, remove", 404)


@api_view(['POST'])
@parser_classes([JSONParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def AddPost(request):
    a = Database()
    t = request.data["title"]
    c = request.data["content"]
    au = request.data["author"]
    return Response(a.add_new_post(t, c, au))


@api_view(["GET"])
def PhotosOfPost(request, post_id):
    photos = Multimedia.objects.all().filter(post_id=post_id)
    serializer = MultimediaSerializer(photos, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def PhotosOfMember(request, id):
    photos = Multimedia.objects.all().filter(members_id=id)
    serializer = MultimediaSerializer(photos, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes([JSONParser])
def PublishPost(request, id):
    a = Database()
    return Response(a.pulish_post(id, bool(request.data["choice"])))

@api_view(['GET'])
def Tags_of_Post(request,id):
    tags = Tags.objects.all().filter(post = id)
    serializer = TagsSerializer(tags,many=True)
    return Response(serializer.data)


@api_view(['GET'])
#@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def Events(request):
    events = Post.objects.all().filter(event = True)
    serializer = PostSerializer(events,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Filter_By_Tags(request,tag):
    tags = get_object_or_404(Tags,tagi__contains = tag)
    posts = Post.objects.all().filter(tag = tags.id)
    serializer = PostSerializer(posts,many=True)
    if len(serializer.data) > 0:
        return Response(serializer.data)
    else:
        return Response({'Response': 'Brak wyniku wyszukiwania'})


@api_view(['GET'])
def Search_query(request,query):
    posts = Post.objects.all().filter(content__contains = query)
    serializer = PostSerializer(posts,many=True)
    if len(serializer.data) > 0:
        return Response(serializer.data)
    else:
        return Response({'Response':'Brak wyniku wyszukiwania'})

@api_view(['GET'])
def Galleries_view(request):
    galleries = Galery.objects.all()
    serializer = GallerySerializer(galleries,many=True)
    return Response(serializer.data)


@api_view(["POST"])
@parser_classes([JSONParser])
def registration(request):
    nick = request.data["nick"]
    name = request.data["name"]
    surname = request.data["surname"]
    email = request.data["email"]
    number = request.data["number"]
    wydzial = request.data["wydzial"]
    kierunek = request.data["kierunek"]
    rok = request.data["rok"]
    template = render_to_string("mail.html",
                                    {"nick":nick,
                                     "name":name,
                                     "surname":surname,
                                     "email":email,
                                     "number":number,
                                     "wydzial":wydzial,
                                     "kierunek":kierunek,
                                     "rok":rok})
    a = Database()
    a.new_registration(nick, name, surname, email, number, wydzial, kierunek, rok)
    return Response(send_mail(
                        "Dane zgłoszeniowe {} {}".format(name, surname), # subject
                        template,  # message
                        settings.EMAIL_HOST_USER,  # from mail
                        ["michael1@opoczta.pl"],  # to mail
                        ))