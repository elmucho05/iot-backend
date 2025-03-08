from rest_framework import serializers
from .models import User
from .models import Compartment1

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compartment1
        fields = '__all__'

