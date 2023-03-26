from rest_framework import serializers
from .models import *


class TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Types
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productimages
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    types = TypesSerializer()
    category = CategorySerializer()
    size = SizeSerializer()
    productimages = ProductImagesSerializer(source='product_images', many=True)

    class Meta:
        model = Product
        fields = '__all__'
