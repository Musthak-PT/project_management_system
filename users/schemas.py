from rest_framework import serializers
from users.models import User

class LoginResponseSchema(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','email','username','is_superuser']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas