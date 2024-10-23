from django.shortcuts import render

# SIMPLE JWT IMPORTS 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# Rest Framework imports
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

# Import Serializers
from .serializers import UserRegisterSerializer, UserLoginSerializer, ServiceSerializer, ProfileSerializer

# Import Models
from .models import Profile, Service

# AllAuth imports 
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter

from dj_rest_auth.registration.views import SocialLoginView

def home(request):
    return render(request, 'app/home.html')

# Service Apis 
# List all services and create a new service
class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
# Retrive, update, or delete a specific service
class ServiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

# Rest-Framework classes
class UserLoginAPIView(TokenObtainPairView):
    
    serializer_class = TokenObtainPairSerializer
    
    def post(self, request, *args, **kargs):
        serializer = self.serializer_class(data=request.data)
        
        try: 
        
            if serializer.is_valid():
                user = User.objects.get(username=request.data['username'])
                try:
                    profile = Profile.objects.get(user=user)
                    profile_data = ProfileSerializer(profile).data
                except Profile.DoesNotExist:
                    profile_data = None
                    
                response = {
                    'success' : True,
                    'id' : user.pk,
                    'username' : user.username,
                    'email' : user.email,
                    'first_name' : user.first_name,
                    'last_name' : user.last_name,
                    'profile': profile_data,
                    'tokens' : serializer.validated_data, # access and refresh tokens
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response({
                
                        'detail' : "Invalid credentials"
                    }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"Detail" : "User does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # create the profile and assign the user_type
            user_type = request.data.get('user_type', 'client') # Default to 'client'
            Profile.objects.create(user=user, user_type=user_type)
            
            # Generate JWT tokens for the newly registered user
            refresh = RefreshToken.for_user(user)
            
            response = {
                'success' : True,
                'user' : serializer.data,
                'profile': {
                    'user_type' : user_type
                },
                'token' : {
                    'refresh' : str(refresh),
                    'access' : str(refresh.access_token)
                }
            }
            
            return Response(response, status=status.HTTP_201_CREATED)
        
        raise ValidationError(
            serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE
        )



class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        
        try: 
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"Success": True, "detail" : "Logged out !"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Success" : False, "detail" : str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def token(request):
    return Response("passed for {}".format(request.user.username))

# Social login view with basic simple jwt
class SocialLoginView(APIView):
    def post(self, request, *args, **kwargs):
        # Logic to authenticate user via social provider (Google/Github)
        user = request.user
        
        # Issue JWT tokens
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh' : str(refresh),
                'access' : str(refresh.access_token),
                })
        return Response({'detail': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
    

# Social login view with dj-rest-auth
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    
    def get_response(self):
        resposne = super().get_response()
        refresh = RefreshToken.for_user(self.user)
        data = {
            'refresh' : str(refresh),
            'access': str(refresh.access_token),
        }