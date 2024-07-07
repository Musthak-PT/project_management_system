from rest_framework import serializers

from tasks.models import Task

class TasksResponseSchema(serializers.ModelSerializer):
    class Meta:
        model= Task
        fields = '__all__'
        
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas