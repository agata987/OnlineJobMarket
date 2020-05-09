from rest_framework import serializers
from ..models import *
from django.contrib.auth import get_user_model


# user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'password', 'first_name','last_name','phone','is_job_seeker','is_employee','description','is_active','is_superuser']

# register user

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name','last_name']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    
    def save(self):
        user_obj = User (
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
        )
        password = self.validated_data['password']
        user_obj.set_password(password)
        user_obj.save()
        return user_obj



# city

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


# comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


# country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


# job offer

class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = '__all__'
