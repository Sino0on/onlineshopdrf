from django.urls import path
from .views import *


urlpatterns = [
    path('product/list/', ProductListView.as_view()),
    path('color/list/', ColorListView.as_view()),
    path('types/list/', TypesListView.as_view()),
    path('category/list/', CategoryListView.as_view()),
    path('size/list/', SizeListView.as_view()),
    path('product/detail/<int:pk>', ProductDetailView.as_view())
]