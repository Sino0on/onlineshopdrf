import django_filters
from .models import *
from django_filters.rest_framework.filters import OrderingFilter
import rest_framework


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='istartswith')
    price = django_filters.NumberFilter()
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_to = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    # ordering = OrderingFilter(fields=('price', 'likes'))

    class Meta:
        model = Product
        ordering = ['id']
        fields = ['title', 'types', 'size', 'category', 'price']

