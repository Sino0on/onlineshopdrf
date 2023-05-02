from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'mailings', 'date_of_birth', 'gender']

    def create(self, validated_data):
        try:
            date = validated_data['date_of_birth']
        except:
            date = None
        try:
            gender = validated_data['gender']
        except:
            gender = None

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mailings=validated_data['mailings'],
            date_of_birth=None,
            gender=gender
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender')

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        print(user)
        return super().update(instance, validated_data)


class ListProductSerializer(serializers.Serializer):
    goods = serializers.JSONField()

    def create(self, validated_data):
        for i in validated_data['goods']:
            print(i)
        return {'Привет': 'Привет'}


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    goods = serializers.JSONField()

    def create(self, validated_data):
        products = []
        for i in validated_data['goods']:
            product = Product.objects.get(id=int(i['product']))
            order = OrderProduct.objects.create(product=product, quantity=i['quantity'])
            order.save()
            products.append(order)


        print(validated_data)
        order = Order.objects.create(
            is_delivery=validated_data['is_delivery'],
            email=validated_data['email'],
            address=validated_data['address'],
            city=validated_data['city'],
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            pay_with_card=validated_data['pay_with_card'],
            gift=validated_data['gift'],
        )
        for i in products:
            order.goods.add(i)
        order.save()
        return order

    class Meta:
        model = Order
        fields = [
            'is_delivery',
            'email',
            'address',
            'city',
            'phone_number',
            'goods',
            'full_name',
            'pay_with_card',
            'gift'
        ]
