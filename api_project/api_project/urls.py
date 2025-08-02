from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token  # Add this import

urlpatterns = [
    path('api/', include('api.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # Updated this line
]
