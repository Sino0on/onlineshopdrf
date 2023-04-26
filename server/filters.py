import django_filters
from .models import *


class ProductFilter(django_filters.FilterSet, django_filters.OrderingFilter):
    title = django_filters.CharFilter(lookup_expr='istartswith')
    price = django_filters.NumberFilter()
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__to = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    ordering = django_filters.OrderingFilter(fields=('price', 'likes'))

    class Meta:
        model = Product
        fields = ['title', 'types', 'size', 'category', 'price', 'ordering']

