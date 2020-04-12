from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from .serializers import *
from ..models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

# user

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('password','email','first_name','last_name','telephone','is_job_seeker','is_employee','is_active','is_superuser')
    ordering_fields = ('email','first_name','last_name','is_job_seeker','is_employee','is_active')
    search_fields = ('email','first_name','last_name')


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# city

class CityList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('name','id_country_id')
    ordering_fields = ('name')


class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


# comment

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('date_published','text','is_blocked','id_job_offer_id','id_user_id')
    ordering_fields = ('date_published')
    search_fields = ('text','date_published')


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# country

class CountryList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('name')
    ordering_fields = ('name')


class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


# offer

class OfferList(generics.ListCreateAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('name','company','full_time','remote','description','id_city_id','id_employee_id')
    ordering_fields = ('name','company','full_time','remote','description','id_city_id','id_employee_id')
    search_fields = ('name','company','description')


class OfferDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
