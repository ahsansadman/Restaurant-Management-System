from django.urls import path, re_path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('api/menu/', views.MenuList.as_view()),
    # path('restaurant/signup/', views.signup),
    # path('restaurant/api/outdoor/menu/', views.OutdoorMenuList.as_view()),
    # path('restaurant/api/indoor/menu/', views.IndoorMenuList.as_view()),
    path('api/orders/', views.OrderList.as_view()),
    # path('restaurant/api/orders/kitchen/', views.KitchenOrderList.as_view()),
    # path('restaurant/api/orders/kabab/', views.KababOrderList.as_view()),
    # path('restaurant/api/orders/coffee/', views.CoffeeOrderList.as_view()),
    path('api/orders/<str:station>/', views.CookingStationOrderList.as_view()),
    path('api/order/<int:pk>/', views.OrderDetail.as_view()),
    path('api/orders/items/<int:pk>/', views.OrderItemDetail.as_view()),
    path('api/register/', views.Register.as_view()),
    # path('restaurant/api/token/<str:username>/', views.TokenView.as_view()),
    path('api/user/', views.UserDetail.as_view()),
]