from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet

from reviews.models import User, Category, Genre, Title, Review
from api_yamdb.settings import ADMIN_EMAIL
from .serializers import (NotAdminSerializer,  UserSerializer,
                          SignupSerializer, TokenSerializer,
                          CategorySerializer, GenreSerializer,
                          TitleSerializer,
                          ReviewSerializer, CommentSerializer
                          )
from .permissions import AdminOnly, IsAuthorAdminModerOrReadOnly


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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class TitleFilter(FilterSet):
    class Meta:
        model = Title
        fields = ['genre__slug', 'category__slug']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('name', 'year')
    filter_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorAdminModerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))  # не уверен!
        return title.reviews

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Нельзя изменить чужой отзыв!')
        super(ReviewViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Нельзя удалить чужой отзыв!')
        super(ReviewViewSet, self).perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Нельзя изменить чужой комментарий!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Нельзя удалить чужой комментарий!')
        super(CommentViewSet, self).perform_destroy(instance)

