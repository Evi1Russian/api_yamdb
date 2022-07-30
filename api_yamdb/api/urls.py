
from rest_framework import routers
from django.urls import include, path

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from .views import (UserViewSet, signup, token)

router = routers.DefaultRouter()

router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token'),
]
