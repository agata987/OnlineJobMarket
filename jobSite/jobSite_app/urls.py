from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('my_account/',views.my_account,name="my_account"),
    path('register/',views.register,name='register'),
    path('edit/',views.edit,name='edit'),
    path('offer_detail/<int:id>/',views.offer_detail,name="offer_detail"),
    path('my_offers',views.my_offers,name="my_offers"),
    path('create_offer',views.create_offer,name="create_offer"),
    path('edit_offer/<int:id>/',views.edit_offer,name="edit_offer"),
    path('delete_offer/<int:id>/',views.delete_offer,name="delete_offer"),
    path('',include('django.contrib.auth.urls')),
    ]