from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated, AllowAny
from reviews.models import User, Category, Genre, Title
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
from rest_framework import mixins


from api_yamdb.settings import ADMIN_EMAIL
from .serializers import (NotAdminSerializer, UserSerializer,
                          SignupSerializer, TokenSerializer,
                          CategorySerializer, GenreSerializer,
                          TitleSerializer)
from .permissions import AdminOnly, IsAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminOnly)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)
    pagination_class = LimitOffsetPagination

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """
    Send accesstoken.
    """
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    token = serializer.data['confirmation_code']
    if not default_token_generator.check_token(user, token):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    token = RefreshToken.for_user(user)
    return Response(token.refresh.access_token, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Send confirmation code.
    """
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        send_confirmation(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_confirmation(user):
    """
    Confirmation mail.
    """
    confirmation_code = default_token_generator.make_token(user)
    subject = 'Код подтверждения '
    message = f'{confirmation_code} - ваш код для авторизации'
    admin_email = ADMIN_EMAIL
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)


class ListDestroyCreateViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListDestroyCreateViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'

    # def destroy(self, serializer, pk=None):
    #    queryset = get_object_or_404(Category,
    #                                 slug=self.kwargs.get('category_slug'))
    #    serializer.delete(queryset)

    # @action(methods=['delete', ], detail=False, url_path='<slug:slug>')
    # def delete_categoty(self, request):
    #    queryset = get_object_or_404(Category,
    #                                 slug=self.kwargs.get('category_slug'))
    #    serializer = self.get_serializer(queryset, many=True)
    #    return Response(serializer.data)


class GenreViewSet(ListDestroyCreateViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleFilter(FilterSet):
    class Meta:
        model = Title
        fields = ['genre__slug', 'category__slug']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('name', 'year')
    filter_class = TitleFilter
