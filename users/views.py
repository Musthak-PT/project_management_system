from rest_framework import viewsets
from .models import User
from .serializers import CreateOrUpdateUserSerializer, LoginSerializer, LogoutSerializer
from .schemas import LoginResponseSchema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.generics import GenericAPIView
from project_management.response import ResponseInfo
from rest_framework.response import Response
from rest_framework import generics,status
from django.shortcuts import get_object_or_404
from users.models import User
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
from users.permissions import IsAdmin

#_______________________Create or update user_______________
class CreateOrUpdateUserApiView(generics.GenericAPIView):
    serializer_class = CreateOrUpdateUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        try:
            id = request.data.get('id')
            if id:
                # Update existing user
                instance = get_object_or_404(User, pk=id)
                serializer = self.serializer_class(instance, data=request.data, context={'request': request})
            else:
                # Create new user
                serializer = self.serializer_class(data=request.data, context={'request': request})

            if serializer.is_valid():
                saved_instance = serializer.save()
                serialized_data = serializer.data
                message = "User has been created successfully" if not id else "User has been updated successfully"
                response_data = {
                    "status_code": status.HTTP_201_CREATED if not id else status.HTTP_200_OK,
                    "message": message,
                    "status": True,
                    "data": serialized_data 
                }
                return Response(response_data, status=status.HTTP_201_CREATED if not id else status.HTTP_200_OK)
            else:
                return Response({
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "status": False,
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "status": False,
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#________________________________Login___________________________________________
class LoginAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LoginAPIView, self).__init__(**kwargs)

    serializer_class = LoginSerializer

    def post(self, request):
        try:

            serializer = self.serializer_class(data=request.data)
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            user = auth.authenticate(username=serializer.validated_data.get('username',''), password=serializer.validated_data.get('password',''))
            
            if user:
                serializer = LoginResponseSchema(user, context={"request": request})
                if not user.is_active:
                    data = {'user': {}, 'token': '', 'refresh': ''}
                    self.response_format['status_code'] = status.HTTP_202_ACCEPTED
                    self.response_format["data"] = data
                    self.response_format["status"] = False
                    self.response_format["message"] = "Account Temparary suspended, contact admin"
                    return Response(self.response_format, status=status.HTTP_200_OK)
                else:
                    refresh = RefreshToken.for_user(user)
                    data = {'user': serializer.data, 'token': str(
                        refresh.access_token), 'refresh': str(refresh)}
                    self.response_format['status_code'] = status.HTTP_200_OK
                    self.response_format["data"] = data
                    self.response_format["status"] = True
                    return Response(self.response_format, status=status.HTTP_200_OK)
                
            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"] = "Invalid credentials"
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#_________________________________________Logout________________________________
class LogoutAPIView(GenericAPIView):

    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LogoutAPIView, self).__init__(**kwargs)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.response_format['status'] = True
            self.response_format["message"] = "Success"
            self.response_format['status_code'] = status.HTTP_200_OK
            return Response(self.response_format, status=status.HTTP_200_OK)

        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)