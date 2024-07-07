from rest_framework import serializers
from .models import Project
from users.models import User

#Create or update serializer
class CreateOrUpdateProjectSerializer(serializers.ModelSerializer):
    id            = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=False, help_text="This field is required only when updating API")
    name          = serializers.CharField(required=False)
    description   = serializers.CharField(required=False)
    members       = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'members']

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        members_data    = validated_data.pop('members', [])
        instance        = Project.objects.create(**validated_data)
        instance.members.set(members_data)
        return instance

    def update(self, instance, validated_data):
        instance.name           = validated_data.get('name', instance.name)
        instance.description    = validated_data.get('description', instance.description)
        
        if 'members' in validated_data:
            new_members = validated_data.pop('members', [])
            instance.members.set(new_members)
        
        instance.save()
        return instance
    
#Delete projects
class DeleteProjectApiRequestSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(),required=True)
    class Meta:
        model = Project
        fields= ['id']