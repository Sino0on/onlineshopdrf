from django.urls import path
from .views import *


urlpatterns = [
    path('goods/', ProductListView.as_view()),
    path('good/<int:pk>', ProductDetailView.as_view()),
    path('user/update/<int:pk>', UserUpdateView.as_view()),
    path('register/', UserCreateView.as_view()),
    path('like/<int:pk>', LikeUserView.as_view()),
    path('goodlistcreate/', ProductListCreateView.as_view()),
    path('auth/', NewAuthView.as_view(), name='token_obtain_pair'),
    path('token/verify/', TokenVerifyCustomView.as_view()),
    path('order/create/', OrderCreateView.as_view()),
    path('orders/', OrderListView.as_view()),
    path('user/change_password/', ChangePasswordView.as_view()),
]

