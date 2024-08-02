

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from videoapi.views import VideoViewSet

router = DefaultRouter()
router.register(r'file', VideoViewSet, basename='video')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
