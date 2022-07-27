from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import (UserViewSet, signup)

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
]
