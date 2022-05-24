from django.urls import path, re_path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('inventory/api/items/', views.InventoryList.as_view()),
    # path('inventory/api/update/order/<int:pk>/', views.UpdateInventory.as_view()),
]