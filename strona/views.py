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


def home(request):
    print('czesc')
    a = Database()
    print(a.comments_of_post(1))
    return render(request, 'Home.html')


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