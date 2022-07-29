from rest_framework import viewsets
# from django.shortcuts import get_object_or_404
# from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
# from rest_framework import mixins


from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer
from .serializers import TitleSerializer


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
