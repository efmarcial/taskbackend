from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from  .models import Profile, Service

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Profile
        fields = ['id', 'user', 'user_type']
        

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'duration']
    
class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta: 
        model = User
        fields = ["id", "username", "password"]
        
class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True)
    user_type = serializers.ChoiceField(choices=Profile.USER_TYPE_CHOICES)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']
        extra_kwargs = {"password" : {'write_only' : True}}
        
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user