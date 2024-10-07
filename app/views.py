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
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

def home(request):
    return render(request, 'app/home.html')

# Rest-Framework classes
class UserLoginAPIView(TokenObtainPairView):
    
    serializer_class = TokenObtainPairSerializer
    
    def post(self, request, *args, **kargs):
        serializer = self.serializer_class(data=request.data)
        
        try: 
        
            if serializer.is_valid():
                user = User.objects.get(username=request.data['username'])
                response = {
                    'success' : True,
                    'username' : user.username,
                    'email' : user.email,
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
            
            # Generate JWT tokens for the newly registered user
            refresh = RefreshToken.for_user(user)
            
            response = {
                'success' : True,
                'user' : serializer.data,
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