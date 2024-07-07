from rest_framework import serializers
from .models import Milestone
from projects.models import Project

#Create or update serializer
class CreateOrUpdateMilestoneSerializer(serializers.ModelSerializer):
    id            = serializers.PrimaryKeyRelatedField(queryset=Milestone.objects.all(), required=False, help_text="This field is required only when updating API")
    project       = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(),required=False)
    name          = serializers.CharField(required=False)
    due_date      = serializers.DateField(required=False)

    class Meta:
        model = Milestone
        fields = ['id','project','name','due_date','created_at', 'updated_at']

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        request                 = self.context.get('request')
        instance                = Milestone()
        
        instance.project        = validated_data.get('project')
        instance.name           = validated_data.get('name')
        instance.due_date       = validated_data.get('due_date')
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        request                 = self.context.get('request')
        instance.project        = validated_data.get('project', instance.project)
        instance.name           = validated_data.get('name', instance.name)
        instance.due_date       = validated_data.get('due_date', instance.due_date)
        
        instance.save()
        return instance
    
#Delete Milestone
class DeleteMilestoneApiRequestSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Milestone.objects.all(),required=True)
    class Meta:
        model = Milestone
        fields= ['id']