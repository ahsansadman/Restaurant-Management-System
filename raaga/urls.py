"""raaga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
# from raaga.restaurant.views import home
# from rest_framework.authtoken import views

from restaurant import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path(r'^api/outdoor/menu/$', views.outdoor_menu_list),
    # re_path(r'^api/indoor/menu/$', views.indoor_menu_list),
    # re_path(r'^api/orders/$', views.order_list),
    # re_path(r'^api/outdoor/menu/$', views.OutdoorMenuList.as_view()),
    # re_path(r'^api/indoor/menu/$', views.IndoorMenuList.as_view()),
    # re_path(r'^api/orders/$', views.OrderList.as_view()),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('restaurant/', include('restaurant.urls')),
    path('inventory/', include('inventory.urls')),
    # path('', test.index),
    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^$', views.home, name='home'),
    # path('api-token-auth/', views.obtain_auth_token),
    # path('accounts/', include('allauth.urls')),
    

]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)