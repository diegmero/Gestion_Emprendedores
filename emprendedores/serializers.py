from rest_framework import serializers
from .models import Emprendedor

class EmprendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprendedor
        fields = '__all__'