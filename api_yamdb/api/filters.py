import django_filters

from reviews.models import Title


class TitleFilter(django_filters.rest_framework.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='contains'
    )
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='contains'
    )
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='contains'
    )
    year = django_filters.CharFilter(
        field_name='year'
    )

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']