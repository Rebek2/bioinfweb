from django.urls import path,include
from . import views
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token



router = routers.DefaultRouter()
router.register(r'tags',views.TagsViewSet)
router.register(r'multimedia',views.MultimediaViewSet)
router.register(r'comment',views.CommentViewSet)
router.register(r'members',views.MemberViewSet)
router.register(r'users',views.UserViewSet)
router.register(r"galery", views.GaleryVievSet)
router.register(r"registrtions", views.RegistrationVievSet)

urlpatterns = [
    path('home/',views.home),
    path('formularz/', views.registration),
    path('api/', include(router.urls)),
    path('api-auth/',include('rest_framework.urls')),
    path('comments/post/<int:id>/',views.CommentsOfPost),
    path('photos/post/<int:post_id>',views.PhotosOfPost),
    path('photos/member/<int:id>',views.PhotosOfMember),
    path('tags/post/<int:id>',views.Tags_of_Post),
    path('events',views.Events),
    path('query/<str:query>',views.Search_query),
    path('filter/post/<tag>',views.Filter_By_Tags),
    path('gallery',views.Galleries_view),
    path('auth',obtain_auth_token),
    path('post/<int:id>/',views.get_post),
    path('post/edit/<int:id>', views.post_edit),
    path('post/add-new',views.Add_Posts),
    path('view-posts',views.View_posts),
    path('post/deletion/<int:id>',views.delete_post),
    path('post/deleted',views.GET_DELETED_POSTS),
    path('post/photo-add/<int:id>',views.Photo_add),
    path('photo-delete/<int:photo_id>/post/<int:post_id>',views.Delete_photo),
    path('members-add',views.Members_Post),
    path('members-delete/<int:id>',views.Delete_Member),
    path('comments-get',views.Get_Comments),
    path('comments-delete/<int:id>',views.Edit_Comment),
    path('get-club-members',views.get_club_members),
    path('delete-gallery-photo/<int:id>',views.Delete_galleryPhoto),
    path('gallery/add',views.add_gallery),
    path('gallery/delete/<int:id>',views.Delete_gallery),
    path('tags-operations',views.getTags),
    path('latest-posts',views.latest_posts),
    path('most-viewed',views.most_viewed)

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




