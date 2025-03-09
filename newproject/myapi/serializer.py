from rest_framework import serializers
from django.utils.timezone import now
from .models import User, Compartment1, Compartment2, Compartment3, CompartmentIntake

# ✅ User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# ✅ Base Serializer for Compartments
class BaseCompartmentSerializer(serializers.ModelSerializer):
    compartment_id = serializers.IntegerField(read_only=True)  # Display the fixed ID
    medicine_name = serializers.CharField(read_only=True)  # Display the medicine name

    class Meta:
        fields = ['id', 'compartment_id', 'medicine_name', 'number_of_medicines', 
                  'to_be_repeated', 'orario_medicina', 'orario_mattina', 
                  'orario_pomeriggio', 'orario_sera']

    def validate(self, data):
        """Ensure taken_time is set correctly"""
        if data.get("taken") and not data.get("taken_time"):
            data["taken_time"] = now()  # Auto-assign current time if not provided
        elif not data.get("taken") and data.get("taken_time"):
            raise serializers.ValidationError("'taken_time' must be empty if 'taken' is False.")
        return data

# ✅ Serializer for Compartment1 (compartment_id = 1)
class Compartment1Serializer(BaseCompartmentSerializer):
    class Meta(BaseCompartmentSerializer.Meta):
        model = Compartment1

# ✅ Serializer for Compartment2 (compartment_id = 2)
class Compartment2Serializer(BaseCompartmentSerializer):
    class Meta(BaseCompartmentSerializer.Meta):
        model = Compartment2

# ✅ Serializer for Compartment3 (compartment_id = 3)
class Compartment3Serializer(BaseCompartmentSerializer):
    class Meta(BaseCompartmentSerializer.Meta):
        model = Compartment3

# ✅ Serializer for Medicine Intakes (Tracks doses taken)
class CompartmentIntakeSerializer(serializers.ModelSerializer):
    compartment_name = serializers.CharField(source="compartment.medicine_name", read_only=True)
    compartment_id = serializers.IntegerField(source="compartment.compartment_id", read_only=True)

    class Meta:
        model = CompartmentIntake
        fields = ['id', 'compartment_id', 'compartment_name', 'intake_time', 'taken', 'taken_time']
