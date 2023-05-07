from django.conf import settings
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics, filters as fr, status
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from .models import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import *
from .filters import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, UntypedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenVerifySerializer


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
    queryset = Product.objects.all().distinct()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, fr.OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ['price', 'likes']
    pagination_class = MyCustomPagination

    def get_queryset(self):
        query_set = super().get_queryset().distinct()
        return query_set.distinct()

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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                username=serializer.validated_data['username'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                email=serializer.validated_data['email'],
                mailings=serializer.validated_data['mailings'],
            )
            user.set_password(serializer.validated_data['password'])
            try:
                validate_password(serializer.validated_data['password'], user)
            except ValidationError as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            das = user.save()
            token = TokenObtainPairSerializer()
            token = token.validate({'username': user.username, 'password': serializer.validated_data['password']})
            # print(token)
            token["user"] = UserSerializer(user).data
            # das = TokenObtainSerializer(data={
            #     'username': serializer.validated_data['username'],
            #     'password': serializer.validated_data['password']
            # })
            # if das.is_valid():
            #     print(das.validated_data)
            return Response(token, status=status.HTTP_200_OK)
        errors = serializer.errors
        print(errors)
        return Response(errors, status=status.HTTP_403_FORBIDDEN)


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UpdateUserSerializer


class LikeUserView(generics.GenericAPIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        product = Product.objects.get(id=kwargs['pk'])
        if self.request.user in product.likes.all():
            product.likes.remove(self.request.user)
            return Response('Remove Success', status=status.HTTP_200_OK)
        else:
            product.likes.add(self.request.user)
            return Response('Add Success')


class NewAuthView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # print(serializer.validated_data)
            user = User.objects.get(username=request.data['username'])
            serializer.validated_data['user'] = UserSerializer(user).data

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ProductListCreateView(generics.GenericAPIView):
    serializer_class = ListProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            for i in serializer.validated_data['goods']:
                print(i)
                p = Product.objects.create(
                    title=i['title'],
                    price=i['price'],
                    image=i['image'],
                    size=i['size'],
                    category=i['category'],
                    types=i['types'],
                    color=i['color'],
                )
                p.save()
            return Response('Dastan', status=status.HTTP_200_OK)


class TokenVerifyCustomSerializer(TokenVerifySerializer):
    def validate(self, attrs):
        token = UntypedToken(attrs["token"])

        if (
            api_settings.BLACKLIST_AFTER_ROTATION
            and "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS
        ):
            jti = token.get(api_settings.JTI_CLAIM)
            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                raise ValidationError("Token is blacklisted")

        return {"detail": "Токен действителен", "code": "token_valid"}


class TokenVerifyCustomView(TokenVerifyView):
    serializer_class = TokenVerifyCustomSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        print(serializer.create(serializer.validated_data))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    pagination_class = MyCustomPagination
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
