from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics
from .models import *
from rest_framework.permissions import IsAdminUser
from .serializers import *
from .filters import *


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter


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
