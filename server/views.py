from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics, filters as fr
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import *
from rest_framework.permissions import IsAdminUser
from .serializers import *
from .filters import *


class MyCustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response({
            # 'links': {
            #     'next': self.get_next_link(),
            #     'previous': self.get_previous_link()
            # },
            'total': self.page.paginator.count,
            'page': self.page.number,
            # 'pages': ,
            'limit': self.get_page_size(self.request),
            'results': data
        })


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.select_related('category', 'color', 'types', 'size').all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, fr.OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ['price', 'likes']
    queryset = Product.objects
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


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
