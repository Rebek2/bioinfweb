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
import datetime
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

@api_view(['GET'])
def get_post(request,id):
    try:
        post = Post.objects.get(id=id)
    except:
        return Response({'Response':'No data'})

    if request.method == 'GET':
        post.add_view()
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)





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
    serializer_class = GallerySerializer

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
    tg = request.data["tagi"]
    ch = request.data["choice"]
    return Response(a.add_new_post(t, c, au, ch, tg), send_mail("subject",
                                                         "message",
                                                          settings.EMAIL_HOST_USER,
                                                          [a.return_mails_of_users()])
)

@api_view(["GET","PUT",'POST'])
def PhotosOfPost(request, post_id):
    photos = Multimedia.objects.all().filter(post_id=post_id)
    if request.method == 'GET':
        serializer = MultimediaSerializer(photos, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = MultimediaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
        photos = Multimedia.objects.all().filter(post_id = post_id)
        serializer2 = MultimediaSerializer(photos, many=True)
        return Response(serializer2.data)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Photo_add(request,id):
    if request.method == 'POST':

        post = Post.objects.get(id=id)
        files = request.FILES.getlist('photos')
        for file in files:
            photo_instance = Multimedia(photos = file,post=post)
            photo_instance.save()
        photos = Multimedia.objects.all().filter(post=post)
        serializer = MultimediaSerializer(photos,many=True)
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
    tags = Tags.objects.get(tagi = tag)
    posts = Post.objects.all().filter(tag = tags.id)
    serializer = PostSerializer(posts,many=True)
    if len(serializer.data) > 0:
        return Response(serializer.data)
    else:
        return Response({'Response': 'Brak wyniku wyszukiwania'})



@api_view(['GET','DELETE','PUT','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Posts(request,id):
    try:
        post = Post.objects.get(id=id)
    except:
        return Response({'Response':'Brak danych'})
    if request.method == 'DELETE':
        post.publish = False
        post.save()

        posts = Post.objects.all().filter(publish = True)
        serializer = PostSerializer(posts,many=True)


        return Response(serializer.data)

    if request.method == 'PUT':

        serializer = PostSerializer(post,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)



@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Add_Posts(request):
    if request.method == 'POST':
        title = request.data['title']
        content = request.data['content']
        author = request.data['author']
        event = request.data['event']
        tags = request.data['tag']
        formated = tags.split(',')
        print(formated)
        if event == 'true':
            event = True
        else:
            event = False

        new_post = Post(title = title,content=content,author=author,event=event)

        new_post.save()

        post = Post.objects.get(id=new_post.id)
        files = request.FILES.getlist('photos')

        for tag in formated:
            tagg = Tags.objects.get(tagi=tag)
            print(tag)
            tagg.post_set.add(post)

        for file in files:
            photo_instance = Multimedia(photos=file, post=post)
            photo_instance.save()



        return Response({'OK':'OK'})



@api_view(['GET'])
def View_posts(request):
    posts = Post.objects.all().filter(publish = True)
    if request.method == 'GET':
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)







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
    if request.method == 'POST':
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
        a.new_registration(nick,
                           name,
                           surname,
                           email,
                           number,
                           wydzial,
                           kierunek,
                           rok)

        send_mail("Dane zgłoszeniowe {} {}".format(name, surname), # subject
                            template,  # message
                            settings.EMAIL_HOST_USER,  # from mail
                            ["adamek0222@gmail.com"],)

        return Response({'OK':'OK'})



@api_view(['DELETE','PUT'])
def delete(request,id):
    try:
        post = Post.objects.get(id=id)
    except:
        return Response({'Response':'Brak danych'})
    if request.method == 'DELETE':
        post.delete()
        posts = Post.objects.all().filter(publish=False)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method =='PUT':
        post.publish = True
        post.save()
        posts = Post.objects.all().filter(publish=False)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def GET_DELETED_POSTS(request):
    posts = Post.objects.all().filter(publish = False)
    if request.method == 'GET':
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)

@api_view(['DELETE'])
def Delete_photo(request,photo_id,post_id):
    try:
        photo_instance = Multimedia.objects.get(id=photo_id)

    except:
        return Response({'Response': 'No data'})
    if request.method=='DELETE':
        photo_instance.delete()
        photos = Multimedia.objects.all().filter(post=post_id)
        serializer = MultimediaSerializer(photos,many=True)
        return Response(serializer.data)



@api_view(['POST','GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Members_Post(request):
    members = Members.objects.all()
    if request.method == 'POST':

        serializer = MembersSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.save()
            file = request.FILES['member_photo']
            photo = Multimedia(photos=file,members = id)
            photo.save()

        serializer = MembersSerializer(members,many=True)
        return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Delete_Member(request,id):
    try:
        member = Members.objects.get(id=id)
    except:
        return Response({'Response': 'Brak danych'})
    if request.method == "DELETE":
        member.delete()
        members = Members.objects.all()
        serializer = MembersSerializer(members,many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Get_Comments(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments,many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Edit_Comment(request,id):
    try:
        comment = Comment.objects.get(id=id)
    except:
        return Response({'Response':'No data'})

    if request.method == 'DELETE':
        comment.delete()
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_club_members(request):
    members = Registration.objects.all()
    serializer = RegistrationSerializer(members,many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Delete_galleryPhoto(request,id):
    try:
        photo_instance = Multimedia.objects.get(id=id)
    except:
        return Response({'Response':'No object'})

    if request.method == 'DELETE':
        photo_instance.delete()
        galleries = Galery.objects.all()
        serializer = GallerySerializer(galleries, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_gallery(request):
    if request.method == 'POST':
        title = request.data['title']
        gallery = Galery(OpisGalerii = title)
        gallery.save()
        gallery_instance = Galery.objects.get(id=gallery.id)
        files = request.FILES.getlist('photos')
        for file in files:
            photo_instance = Multimedia(photos=file,gallery=gallery_instance)
            photo_instance.save()

        return Response({'Ok':'Ok'})

@api_view(['DELETE','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Delete_gallery(request,id):
    try:
        gallery = Galery.objects.get(id=id)
    except:
        return Response({'Response':'No object in db'})
    if request.method == 'DELETE':
        gallery.delete()
        photos = Galery.objects.all()
        serializer = GallerySerializer(photos,many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        files = request.FILES.getlist('photos')
        for file in files:
            photo_instance = Multimedia(gallery=gallery,photos=file)
            photo_instance.save()
        photos = Galery.objects.all()
        serializer = GallerySerializer(photos,many=True)
        return Response(serializer.data)

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getTags(request):
    if request.method == 'GET':
        tags = Tags.objects.all()
        serializer = TagsSerializer(tags,many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        name = request.data['tagi']
        tag_instance = Tags(tagi=name)
        tag_instance.save()
        tags = Tags.objects.all()
        serializer = TagsSerializer(tags,many=True)
        return Response(serializer.data)
