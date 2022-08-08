from rest_framework import routers
from django.urls import include, path

from .views import (UserViewSet, signup, token,
                    CategoryViewSet, GenreViewSet, TitleViewSet,
                    ReviewViewSet, CommentViewSet
                    )

router = routers.DefaultRouter()

router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UserViewSet, basename='users')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet,
                basename='reviews'
                )
router.register(r'titles/(?P<title_id>\d+)'
                r'/reviews/(?P<review_id>\d+)'
                r'/comments',
                CommentViewSet,
                basename='comments'
                )

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token'),
]
