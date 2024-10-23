
from django.urls import path, include
from . import views
from .views import UserLoginAPIView, UserRegisterAPIView, UserLogoutAPIView, token, ServiceDetailAPIView, ServiceListCreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
   path('', views.home, name='home'),
   path('login/', UserLoginAPIView.as_view(), name='user_login'),
   path('register/', UserRegisterAPIView.as_view(), name="user_register"),
   path('logout/', UserLogoutAPIView.as_view(), name='logout'),
   path('token/', token, name='token' ),
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('api/auth/', include('dj_rest_auth.urls')),  # For login, logout, password reset, etc.
   path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # For registration and social login
   path('api/services/', ServiceListCreateAPIView.as_view(), name="service-list_create"),
   path('api/services/<int:pk>/', ServiceDetailAPIView.as_view(), name="service-detail"),
]

# Use the token for Frontend Application Access
# Include the token in the header of your API request in 
# the following format: 

# Authorization: Token <your_token>