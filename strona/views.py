from django.shortcuts import render, redirect
from .serializer import *
from rest_framework import viewsets
from .DAL import Database
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, parser_classes,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
import facebook
import requests
import os
from wsgiref.util import FileWrapper
from rest_framework import generics


class FB_manager:
    def __init__(self):
        self.is_facebook_active = False
        self.page_id = settings.PAGE_ID
        self.access_token = settings.FACEBOOK_ACCESS_TOKEN
        self.app_id = settings.FACEBOOK_APP_ID
        self.dal = Database()

    def automation(self, files, post_id):
        if not self.is_facebook_active:
            return
        msg = self.dal.fetch_post_values(post_id)
        files_raw = []
        for file in files:
            files_raw.append(file)

        graph = facebook.GraphAPI(self.access_token)
        if len(files_raw)<1:
            fb_id = graph.put_object(parent_object="me", connection_name="feed",message=msg)
        else:
            fb_id = graph.put_photo(image=open(r"./media/photos/{}".format(str(files_raw[0])), "rb"),
                                    message=msg)

        fb_post_id = str(fb_id["id"])
        post = self.dal.retrieve_post_by_id(post_id)
        post.facebook_id = fb_post_id
        post.save()

    def post_deletetion(self, post_id):
        if not self.is_facebook_active:
            return
        post = self.dal.retrieve_post_by_id(post_id)

        graph = facebook.GraphAPI(self.access_token)
        try:
            graph.delete_object(id=str(post.facebook_id))
        except facebook.GraphAPIError:
            post.facebook_id = 'None'
            post.save()

        post.facebook_id = 'None'
        post.save()

    def fetch_data_post(self, post_id):
        if not self.is_facebook_active:
            return
        post = self.dal.retrieve_post_by_id(post_id)

        graph = facebook.GraphAPI(self.access_token)
        data_graph = graph.get_object(post.facebook_id)

        return data_graph

    def edit_post(self, post_id):
        if not self.is_facebook_active:
            return
        post = self.dal.retrieve_post_by_id(post_id)
        mess = self.dal.fetch_post_values(post_id)
        adress = "https://graph.facebook.com/v16.0/{}?message={}%20wiadomosc&access_token={}"
        url = adress.format(post.facebook_id, mess, self.access_token)
        return requests.post(url)

    def get_access_permanent(self, app_secret, short_token):
        if not self.is_facebook_active:
            return
        urluno = "https://graph.facebook.com/v15.0/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(self.app_id, app_secret, short_token)
        token = requests.get(urluno).json()
        return token["access_token"]


def home(request):
    print('czesc')
    a = Database()
    print(a.return_mails_of_users())
    #print(FB_manager().fetch_data_post(9))
    #print(a.add_comms_from_FB(FB_manager().fetch_data_post(2),"111016638421384_127474316787981"))
    #print(FB_manager().fetch_data_post(2))
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
    serializer_class = GallerySerializer


class RegistrationVievSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


class DownloadableViewSet(viewsets.ModelViewSet):
    queryset = Downloadable.objects.all()
    serializer_class = DownloadableSerializer


@api_view(['GET'])
def get_post(request, id):
    try:
        post = Post.objects.get(id=id)
    except:
        return Response({'Response':'No data'})
    if request.method == 'GET':
        #Database().add_comms_from_FB(FB_manager().fetch_data_post(id),post.facebook_id)
        post.add_view()
        post.save()

        serializer = PostSerializer(post)
        return Response(serializer.data)

@api_view(['GET'])
def CommentsOfPost(request,id):
    comments = Comment.objects.all().filter(post_id = id)
    serializer = CommentSerializer(comments,many=True)
    return Response(serializer.data)


@api_view(["GET","PUT",'POST'])
def PhotosOfPost(request, post_id):
    photos = Multimedia.objects.all().filter(post_id=post_id)
    if request.method == 'GET':
        serializer = MultimediaSerializer(photos, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MultimediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        photos = Multimedia.objects.all().filter(post_id = post_id)
        serializer2 = MultimediaSerializer(photos, many=True)
        return Response(serializer2.data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_edit(request, id):
    a = Database()
    try:
        post = a.retrieve_post_by_id(id=id)
    except:
        return Response({'Response':'Brak danych'})

    if request.method == 'DELETE':
        post.publish = False

        FB_manager().post_deletetion(post.id)
        post.save()

        posts = Post.objects.all().filter(publish = True)
        serializer = PostSerializer(posts,many=True)

        return Response(serializer.data)

    if request.method == 'PUT':
        title = request.data['title']
        content = request.data['content']
        author = request.data['author']
        event = request.data['event']
        #tags = request.data['tag']
        print(post.tag.all())
        tags = ",".join([x.tagi for x in post.tag.all()])
        #publish = request.data['publish']
        publish = post.publish
        #photo = request.FILES.getlist('photos')
        photo = post.photos

        if event == 'true' or event == "True" or event == True or event == 1:
            event = True
        else:
            event = False

        if publish == 'true' or publish == "True" or publish == True or publish == 1:
            publish = True
        else:
            publish = False

        a.modify_post_by_id(id, title, content, author, event, tags, publish, photo)
        raw_photos = []

        if publish == True:
            for item in photo:
                raw_photos.append(item)
            if post.facebook_id == "None":
                FB_manager().automation(raw_photos, post.id)
            elif post.facebook_id != "None":
                FB_manager().post_deletetion(id)
                FB_manager().automation(raw_photos, post.id)
        elif publish == False:
            if str(post.facebook_id) != 'None':
                FB_manager().post_deletetion(id)
            else:
                print("no")

        return Response({"ok":"ok"})
    return Response({'ok':'ok'})


@api_view(['GET','POST'])
#@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def Add_Posts(request):
    base = Database()
    if request.method == 'POST':
        title = request.data['title']
        content = request.data['content']
        author = request.data['author']
        event = request.data['event']
        tags = request.data['tag']
        if event == 'true' or event == "True" or event == True or event == 1:
            event = True
        else:
            event = False
        content = content.replace("\n", "<br>")

        new_post = base.add_new_post(title, content, author, True, tags, event)

        post = Post.objects.get(id=new_post)
        files = request.FILES.getlist('photos')
        raw_files_names = []
        for file in files:
            photo_instance = Multimedia(photos=file, post=post)
            photo_instance.save()
            raw_files_names.append(file)

        FB_manager().automation(raw_files_names, new_post)
        template_news = render_to_string("newsletter.html",
                                         {"title": title,
                                          "author": author})

        send_mail("Newsletter koła bioinformatyków",#title
                  template_news,#content
                  settings.EMAIL_HOST_USER,#mail from
                  base.return_mails_of_users(), #its returns list, soo there is no need for another parenthesis
                  fail_silently=True)

        return Response({'OK':'OK'})
    return Response({'OK': 'OK'})


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


@api_view(['GET'])
def Tags_of_Post(request,id):
    tags = Tags.objects.all().filter(post = id)
    serializer = TagsSerializer(tags,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Events(request):
    events = Post.objects.all().filter(event = True,publish = True)
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


@api_view(['GET'])
def View_posts(request):

    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 3

        posts = Post.objects.all().filter(publish=True)
        result_page = paginator.paginate_queryset(posts, request)

        serializer = PostSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)

@api_view(['DELETE', 'PUT'])
def delete_post(request, id):
    try:
        post = Database().retrieve_post_by_id(id)
    except:
        return Response({'Response':'Nie istniejacy wpis'})
    if request.method == 'DELETE':
        post.delete()
        posts = Post.objects.filter(publish=False)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

@api_view(['PUT'])
def post_restore(request, id):
    try:
        post = Database().retrieve_post_by_id(id)
    except:
        return Response({'Response': 'Nie istniejacy wpis'})
    if request.method == 'PUT':
        post.publish = True
        post.save()
        # post.delete()
        posts = Post.objects.filter(publish=False)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    if request.method == 'PUT':
        posts = Post.objects.filter(pu)
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


@api_view(['POST'])
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
        subscription = request.data["subscription"]
        template = render_to_string("mail.html", {"nick": nick,
                                                  "name": name,
                                                  "surname": surname,
                                                  "email": email,
                                                  "number": number,
                                                  "wydzial": wydzial,
                                                  "kierunek": kierunek,
                                                  "rok": rok})
        a = Database()
        a.new_registration(nick,
                           name,
                           surname,
                           email,
                           number,
                           wydzial,
                           kierunek,
                           rok,
                           subscription)
        send_mail("Dane zgłoszeniowe {} {}".format(name, surname),  # subject
                  template,  # message
                  settings.EMAIL_HOST_USER,  # from mail
                  ["nswa87@gmail.com"]+ a.fetch_club_court_mails() , #to mails
                  fail_silently=False)

        return Response({'OK': 'OK'})

    return Response({"OK":"NOK"})


@api_view(['GET'])
def GET_DELETED_POSTS(request):
    posts = Post.objects.all().filter(publish=False)
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
        inst = str(photo_instance.photos).split("photos/")
        photo_instance.delete()
        if os.path.exists(r"media/photos/{}".format(inst)):
            os.remove(r"media/photos/{}".format(inst))
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

    if request.method == 'POST':
        comm = request.data["comment"]
        Database().modify_comment_by_id(id, comm)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_club_members(request):
    members = Registration.objects.all()
    serializer = RegistrationSerializer(members,many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
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
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
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

@api_view(['GET','DELETE', 'PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getTags(request):
    if request.method == 'GET':
        tags = Tags.objects.all()
        serializer = TagsSerializer(tags,many=True)
        return Response(serializer.data)

    if request.method == 'PUT':
        names = request.data['tagi']
        tags = Database().add_tags(names)
        serializer = TagsSerializer(tags,many=True)
        return Response(serializer.data)

    if request.method == "DELETE":
        Database().clear_unused_tags()
        serializer = TagsSerializer(Database().fetch_tags(True), many=True)
        return Response(serializer.data)



@api_view(['GET'])
def latest_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all().filter(publish=True)[:5] #5 last elements from db
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)

@api_view(['GET'])
def most_viewed(request):
    if request.method == 'GET':
        posts = Post.objects.all().filter(publish =True).order_by('-views')[:5]
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)

@api_view(["POST"])
def canceling_subsctiption(request):
    if request.method == "POST":
        user_mail = request.data["e-mail"]
        res = Database().change_subs_status(user_mail)
        return Response({"Status": "{}".format(res)})
    return Response({"ok":"ok"})

@api_view(['POST', 'GET', 'PUT', 'DELETE'])

def downloadable_files(request):
    if request.method == "POST":
        file_name = request.data['name']
        upload = request.FILES["upload"]
        status = Database().downloads_add(file_name, upload)
        return Response({"Status":status})

    if request.method == "GET":
        downs = Downloadable.objects.all()
        serializer = DownloadableSerializer(downs, many=True)

        return Response(serializer.data)

    if request.method == "PUT":
        file_name = request.data['id']
        upload = request.FILES["upload"]
        status = Database().downloads_edit(file_name, upload)
        return Response({"Status":status})

    if request.method == "DELETE":
        file_id = request.data['id']
        status = Database().downloads_delete(file_id)
        return Response({"Status":status})

    return Response({"Status":'100'})


@api_view(["GET"])
def download_file(request, id):
    if request.method == 'GET':
            queryset = Downloadable.objects.get(id=id)
            file_handle = queryset.upload.path
            document = open(file_handle, 'rb')
            response = HttpResponse(FileWrapper(document), content_type='application/msword')
            response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.upload.name
            Database().downloads_counter(id=id)
            return response

