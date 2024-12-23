"""
Views for the user API
"""
from rest_framework import generics, authentication, permissions

from user.serializers import UserSerializer, AuthTokenSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

#RetrieveUpdateAPIView is provided for retrieveing and updating objects in database
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenicated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user