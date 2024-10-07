
from django.urls import path, include
from . import views
from .views import UserLoginAPIView, UserRegisterAPIView, UserLogoutAPIView, token


urlpatterns = [
   path('', views.home, name='home'),
   path('login/', UserLoginAPIView.as_view(), name='user_login'),
   path('register/', UserRegisterAPIView.as_view(), name="user_register"),
   path('logout/', UserLogoutAPIView.as_view(), name='logout'),
   path('token/', token, name='token' )
]

# Use the token for Frontend Application Access
# Include the token in the header of your API request in 
# the following format: 

# Authorization: Token <your_token>