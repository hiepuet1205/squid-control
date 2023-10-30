from django.urls import path, include
from . import views

urlpatterns = [
    path('proxy/', include('squid.proxy.urls'), name='squid.proxy'),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('', views.index, name='index'),
]
