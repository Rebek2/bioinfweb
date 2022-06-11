from django.urls import path,include
from . import views
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'posts',views.PostViewSet)
router.register(r'tags',views.TagsViewSet)
router.register(r'multimedia',views.MultimediaViewSet)
router.register(r'comment',views.CommentViewSet)
router.register(r'members',views.MemberViewSet)

urlpatterns = [
    path('home/',views.home),
    path('api/', include(router.urls)),
    path('api-auth/',include('rest_framework.urls')),
    path('comments/post/<int:id>/',views.CommentsOfPost),
    path('post/<int:id>', views.UpdatePost),
    path('photos/post/<int:post_id>',views.PhotosOfPost),
    path('photos/member/<int:id>',views.PhotosOfMember),
    path('post/publish/<int:id>', views.PublishPost),
    path('post/add-new', views.AddPost)


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




