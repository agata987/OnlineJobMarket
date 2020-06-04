from rest_framework import generics
from .serializers import *
from ..models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

# user

class UserList(generics.ListCreateAPIView):
   
    # authentication and permissions
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    # filters
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('password','email','first_name','last_name','phone','is_job_seeker','is_employee','is_active','is_superuser')
    ordering_fields = ('email','first_name','last_name','is_job_seeker','is_employee','is_active')
    search_fields = ('email','first_name','last_name')


# register user

@api_view(['POST',])
@permission_classes([AllowAny])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user_obj = serializer.save()
        data['response'] = "New user registered."
        data['email'] = user_obj.email
        data['first_name'] = user_obj.first_name
        data['last_name'] = user_obj.last_name
    else:
        data = serializer.errors
    return Response(data)
    

class UserDetail(generics.RetrieveUpdateDestroyAPIView):

    # authentication and permissions
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


# city

class CityList(generics.ListCreateAPIView):

    # authentication and permissions
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = City.objects.all()
    serializer_class = CitySerializer

    # filters
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('name','id_country_id')
    ordering_fields = ('name')



class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    
    # authentication and permissions
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = City.objects.all()
    serializer_class = CitySerializer

# comment

class CommentList(generics.ListCreateAPIView):
    # authentication and permissions
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # filters
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('date_published','text','is_blocked','id_job_offer_id','id_user_id')
    ordering_fields = ('date_published')
    search_fields = ('text','date_published')


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    # authentication and permissions
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# country

class CountryList(generics.ListCreateAPIView):
    
    # authentication and permissions
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    # filters
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('name',)
    ordering_fields = ('name',)


class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    # authentication and permissions
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


# offer

class OfferList(generics.ListCreateAPIView):
    # authentication and permissions
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer

    # filters
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('name','company','full_time','remote','description','id_city_id','id_employee_id')
    ordering_fields = ('name','company','full_time','remote','description','id_city_id','id_employee_id')
    search_fields = ('name','company','description')



class OfferDetail(generics.RetrieveUpdateDestroyAPIView):
    # authentication and permissions
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer

