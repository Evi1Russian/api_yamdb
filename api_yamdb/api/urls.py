from rest_framework import routers
from django.urls import include, path

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet


router = routers.DefaultRouter()

router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls)),
]
