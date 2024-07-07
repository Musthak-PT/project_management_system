from rest_framework import viewsets
from .models import Project
from .serializers import DeleteProjectApiRequestSerializer, CreateOrUpdateProjectSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .schemas import ProjectsResponseSchema
from rest_framework import filters
from rest_framework.response import Response
from project_management.response import ResponseInfo
from django_acl.utils.helper import get_object_or_none
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.

#_________________________________Listing of projects_______________________
class ProjectListingApiView(generics.ListAPIView):
    queryset = Project.objects.all().order_by('-id')
    serializer_class = ProjectsResponseSchema
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        
        if instance_id:
            queryset = queryset.filter(pk=instance_id)
        
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True, context={'request': request})
        
        return self.get_paginated_response(serializer.data) 
    

#_________________________________create or update of projects_______________________

class CreateOrUpdateProjectsApiView(generics.GenericAPIView):
    serializer_class = CreateOrUpdateProjectSerializer

    def post(self, request):
        try:
            id = request.data.get('id')
            if id:
                # Update existing project
                instance = get_object_or_404(Project, pk=id)
                serializer = self.serializer_class(instance, data=request.data, context={'request': request})
            else:
                # Create new project
                serializer = self.serializer_class(data=request.data, context={'request': request})

            if serializer.is_valid():
                saved_instance = serializer.save()
                serialized_data = self.serializer_class(saved_instance, context={'request': request}).data
                response_data = {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "Project has been created successfully" if not id else "Project has been updated successfully",
                    "status": True,
                    "data": serialized_data 
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
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
            
            
#_________________________________Delete projects_______________________
class DeleteProjectsApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteProjectsApiView, self).__init__(**kwargs)

    serializer_class = DeleteProjectApiRequestSerializer
    # permission_classes = (IsAuthenticated,)

    def delete(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():

                instance = serializer.validated_data.get('id', None)
                instance.delete()

                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format["message"] = "You have deleted SuccessFully"
                self.response_format["status"] = True
                return Response(self.response_format, status=status.HTTP_200_OK)

            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)