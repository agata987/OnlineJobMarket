from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('my_account/',views.my_account,name="my_account"),
    path('register/',views.register,name='register'),
    path('edit/',views.edit,name='edit'),
    path('offer_detail/<int:id>/',views.offer_detail,name="offer_detail"),
    path('create_offer',views.create_offer,name="create_offer"),
    path('',include('django.contrib.auth.urls')),
    ]