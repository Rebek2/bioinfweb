from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts',views.PostViewSet)
router.register(r'tags',views.TagsViewSet)
router.register(r'multimedia',views.MultimediaViewSet)
router.register(r'comennt',views.CommentViewSet)


urlpatterns = [
    path('home/',views.home),
    path('api/', include(router.urls)),
    path('api-auth/',include('rest_framework.urls')),
]