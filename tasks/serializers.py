from rest_framework import serializers
from .models import Task
from projects.models import Project
from users.models import User

#Create or update serializer
class CreateOrUpdateTaskSerializer(serializers.ModelSerializer):
    id            = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False, help_text="This field is required only when updating API")
    project       = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(),required=False)
    name          = serializers.CharField(required=False)
    description   = serializers.CharField(required=False)
    assigned_to   = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=False)
    due_date      = serializers.DateField(required=False)
    status        = serializers.CharField(required=False)

    class Meta:
        model = Task
        fields = ['id','project','name', 'description','assigned_to','due_date','created_at', 'updated_at', 'status']

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        request                 = self.context.get('request')
        instance                = Task()
        instance.project        = validated_data.get('project')
        instance.name           = validated_data.get('name')
        instance.description    = validated_data.get('description')
        instance.assigned_to    = validated_data.get('assigned_to')
        instance.due_date       = validated_data.get('due_date')
        instance.status         = validated_data.get('status')
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        request                 = self.context.get('request')
        instance.project        = validated_data.get('project', instance.project)
        instance.name           = validated_data.get('name', instance.name)
        instance.description    = validated_data.get('description', instance.description)
        instance.assigned_to    = validated_data.get('assigned_to', instance.assigned_to)
        instance.due_date       = validated_data.get('due_date', instance.due_date)
        instance.status         = validated_data.get('status', instance.status)
        
        instance.save()
        return instance
    
#Delete Tasks
class DeleteTasksApiRequestSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(),required=True)
    class Meta:
        model = Task
        fields= ['id']
        

#Assign single task to single users
class AssignTasksSerializer(serializers.ModelSerializer):
    id            = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(),required=True)
    assigned_to   = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=True)
    
    class Meta:
        model = Task
        fields= ['id','assigned_to']