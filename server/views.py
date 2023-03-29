from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import *
from rest_framework.permissions import IsAdminUser
from .serializers import *
from .filters import *


class MyCustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):

        return Response({
            # 'links': {
            #     'next': self.get_next_link(),
            #     'previous': self.get_previous_link()
            # },
            'total': self.page.paginator.count,
            'page': self.page.number,
            # 'pages': ,
            'limit': self.page_size,
            'results': data
        })


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.select_related('category', 'color', 'types', 'size').all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = MyCustomPagination


    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     print(len(queryset.all()))
    #
    #     data = self.serializer_class(queryset, many=True)
    #     data = data.data
    #     print(data)
    #     new_data = {
    #         'items': len(queryset.all()),
    #         'products': data,
    #
    #     }
    #     return Response(new_data)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class ColorListView(generics.ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TypesListView(generics.ListAPIView):
    queryset = Types.objects.all()
    serializer_class = TypesSerializer


class SizeListView(generics.ListAPIView):
    queryset = Types.objects.all()
    serializer_class = SizeSerializer
