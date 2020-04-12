from django.urls import path
from . import views

app_name = "jobSite_app"

urlpatterns = [
    path('users/', views.UserList.as_view(), name='users_list'),
    path('users/<pk>/', views.UserDetail.as_view(), name='user_detail'),

    path('cities/', views.CityList.as_view(), name='cities_list'),
    path('cities/<pk>/', views.CityDetail.as_view(), name='city_detail'),

    path('comments/', views.CommentList, name='comments_list'),
    path('comments/<pk>/', views.CommentDetail.as_view(), name='comment_detail'),

    path('countries/', views.CountryList.as_view(), name='countries_list'),
    path('countries/<pk>/', views.CountryDetail.as_view(), name='country_detail'),

    path('offers/', views.OfferList.as_view(), name='offers_list'),
    path('offers/<pk>/', views.OfferDetail.as_view(), name='offer_detail'),
]
