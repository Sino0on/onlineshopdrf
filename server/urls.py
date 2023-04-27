from django.urls import path
from .views import *


urlpatterns = [
    path('goods/', ProductListView.as_view()),
    path('good/<int:pk>', ProductDetailView.as_view()),
    path('register/', UserCreateView.as_view())
]