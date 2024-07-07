from rest_framework import serializers
from projects.models import Project

class ProjectsResponseSchema(serializers.ModelSerializer):
    class Meta:
        model= Project
        fields= ['id','name','description','created_at','updated_at','members']
        
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas