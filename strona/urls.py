from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posty',views.PostViewSet)



urlpatterns = [
    path('home/',views.home),
    path('api/', include(router.urls)),
    path('api-auth/',include('rest_framework.urls')),
]