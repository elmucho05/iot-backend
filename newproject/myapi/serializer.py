from rest_framework import serializers
from .models import User
from .models import Compartment1, CompartmentIntake
from django.utils.timezone import now

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compartment1
        fields = '__all__'
        
    def validate(self, data):
        """Ensure taken_time is set correctly"""
        if data.get("taken") and not data.get("taken_time"):
            data["taken_time"] = now()  # Auto-assign current time if not provided
        elif not data.get("taken") and data.get("taken_time"):
            raise serializers.ValidationError("'taken_time' must be empty if 'taken' is False.")
        return data



class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compartment1
        fields = '__all__'

class CompartmentIntakeSerializer(serializers.ModelSerializer):
    compartment_name = serializers.CharField(source="compartment.medicine_name", read_only=True)

    class Meta:
        model = CompartmentIntake
        fields = ['id', 'compartment_name', 'intake_time', 'taken', 'taken_time']
