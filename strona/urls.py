from django.urls import path,include
from . import views
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token



router = routers.DefaultRouter()
router.register(r'posts',views.PostViewSet)
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
    path('post/update/<int:id>', views.UpdatePost),
    path('photos/post/<int:post_id>',views.PhotosOfPost),
    path('photos/member/<int:id>',views.PhotosOfMember),
    path('post/publish/<int:id>', views.PublishPost),
    path('post/add-new', views.AddPost),
    path('tags/post/<int:id>',views.Tags_of_Post),
    path('events',views.Events),
    path('query/<str:query>',views.Search_query),
    path('filter/post/<tag>',views.Filter_By_Tags),
    path('gallery',views.Galleries_view),
    path('auth',obtain_auth_token),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




