from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics, filters as fr, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import *
from .filters import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken


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
                gender=serializer.validated_data['gender'],
                date_of_birth=serializer.validated_data['date_of_birth'],
                email=serializer.validated_data['email'],
                mailings=serializer.validated_data['mailings'],
            )
            user.set_password(serializer.validated_data['password'])
            das = user.save()
            token = TokenObtainPairSerializer.get_token(user)
            data = {}
            data["refresh"] = str(token)
            data["access"] = str(token.access_token)
            data["user"] = UserSerializer(user)
            print(data)
            # das = TokenObtainSerializer(data={
            #     'username': serializer.validated_data['username'],
            #     'password': serializer.validated_data['password']
            # })
            # if das.is_valid():
            #     print(das.validated_data)
            return Response(f'{data}', status=status.HTTP_200_OK)
        pass


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