from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="proxy"),
    path('update/<int:id>', views.updateProxy, name="updateProxy"),
    path('delete/<int:id>', views.deleteProxy, name="deleteProxy"),
    path('create-proxy', views.createProxy, name='createProxy'),
    path('update-bandwidth', views.updateBandwidth, name='updateBandwidth'),
]
