from django.urls import path
from . import views as reg_view
from rest_framework.authtoken import views

app_name = "jobSite_app"

urlpatterns = [
    path('users/', reg_view.UserList.as_view(), name='users_list'),
    path('users/<pk>/', reg_view.UserDetail.as_view(), name='user_detail'),

    path('cities/', reg_view.CityList.as_view(), name='cities_list'),
    path('cities/<pk>/', reg_view.CityDetail.as_view(), name='city_detail'),

    path('comments/', reg_view.CommentList, name='comments_list'),
    path('comments/<pk>/', reg_view.CommentDetail.as_view(), name='comment_detail'),

    path('countries/', reg_view.CountryList.as_view(), name='countries_list'),
    path('countries/<pk>/', reg_view.CountryDetail.as_view(), name='country_detail'),

    path('offers/', reg_view.OfferList.as_view(), name='offers_list'),
    path('offers/<pk>/', reg_view.OfferDetail.as_view(), name='offer_detail'),

    path('token-auth/',views.obtain_auth_token,name='token-auth'),
]
