from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics

class UserViewSet(generics.ListAPIView):
    queryset            = User.objects.all()
    serializer_class    = UserSerializer
    permission_classes  = [IsAuthenticated]