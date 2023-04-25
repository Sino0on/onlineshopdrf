import django_filters
from .models import *


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter()
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__to = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ['title', 'types', 'size', 'category', 'price']

