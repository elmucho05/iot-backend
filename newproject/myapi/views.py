from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import (
    UserSerializer, 
    Compartment1Serializer, 
    Compartment2Serializer, 
    Compartment3Serializer, 
    CompartmentIntakeSerializer
)
from .models import User, Compartment1, Compartment2, Compartment3, CompartmentIntake
from django.utils.timezone import localtime, now

def get_compartment_model(compartment_id):
    """Return the correct compartment model based on the given ID."""
    compartments = {
        1: (Compartment1, Compartment1Serializer),
        2: (Compartment2, Compartment2Serializer),
        3: (Compartment3, Compartment3Serializer),
    }
    return compartments.get(compartment_id, (None, None))


@api_view(['GET'])
def get_medicines(request, compartment_id):
    """Retrieve all medicines from a specific compartment."""
    CompartmentModel, Serializer = get_compartment_model(compartment_id)

    if not CompartmentModel:
        return Response({"error": "Invalid compartment ID"}, status=status.HTTP_400_BAD_REQUEST)

    medicines = CompartmentModel.objects.all()
    serializer = Serializer(medicines, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_medicine(request, compartment_id):
    """Create a new medicine entry in the specified compartment."""
    CompartmentModel, Serializer = get_compartment_model(compartment_id)

    if not CompartmentModel:
        return Response({"error": "Invalid compartment ID"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def medicine_detail(request, compartment_id, pk):
    """Retrieve, update, or delete a specific medicine from a compartment."""
    CompartmentModel, Serializer = get_compartment_model(compartment_id)

    if not CompartmentModel:
        return Response({"error": "Invalid compartment ID"}, status=status.HTTP_400_BAD_REQUEST)

    medicine = get_object_or_404(CompartmentModel, pk=pk)

    if request.method == 'GET':
        serializer = Serializer(medicine)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Serializer(medicine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        medicine.delete()
        return Response({"message": "Medicine deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_pending_intakes(request):
    """Retrieve all pending medicine intakes from all compartments."""
    pending_intakes = CompartmentIntake.objects.filter(taken=False).order_by('intake_time')
    serializer = CompartmentIntakeSerializer(pending_intakes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_taken_intakes(request):
    """Retrieve all medicines that have been taken with timestamps."""
    taken_intakes = CompartmentIntake.objects.filter(taken=True).order_by('-taken_time')
    serializer = CompartmentIntakeSerializer(taken_intakes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def mark_intake_as_taken(request, intake_id):
    """Marks a specific intake instance as taken."""
    intake = get_object_or_404(CompartmentIntake, id=intake_id)

    if intake.taken:
        return Response({"message": "This dose has already been taken."}, status=status.HTTP_400_BAD_REQUEST)

    intake.mark_as_taken()
    serializer = CompartmentIntakeSerializer(intake)
    return Response(serializer.data, status=status.HTTP_200_OK)


from django.contrib.contenttypes.models import ContentType

@api_view(['POST'])
def take_medicine_from_compartment(request, comp_id):
    """Marks the next pending intake OR a one-time medicine as taken"""
    
    compartment_models = {1: Compartment1, 2: Compartment2, 3: Compartment3}
    CompartmentModel = compartment_models.get(comp_id)

    if not CompartmentModel:
        return Response({"error": "Invalid compartment ID"}, status=status.HTTP_400_BAD_REQUEST)

    # Try to find a pending repeated medicine intake
    pending_intake = CompartmentIntake.objects.filter(
        compartment_type=ContentType.objects.get_for_model(CompartmentModel),
        taken=False
    ).order_by('intake_time').first()

    if pending_intake:
        pending_intake.mark_as_taken()
        serializer = CompartmentIntakeSerializer(pending_intake)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # If no pending repeated intake, check for a one-time medicine
    one_time_medicine = CompartmentModel.objects.filter(
        to_be_repeated=False, orario_medicina__isnull=False
    ).first()

    if one_time_medicine:
        # Create a one-time intake record and mark it as taken
        new_intake = CompartmentIntake.objects.create(
            compartment_type=ContentType.objects.get_for_model(CompartmentModel),
            compartment_id=one_time_medicine.id,
            intake_time=one_time_medicine.orario_medicina,
            taken=True,
            taken_time=now()
        )
        serializer = CompartmentIntakeSerializer(new_intake)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"message": "No pending intakes or one-time medicines found for this compartment"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def get_pending_intakes_by_compartment(request, comp_id):
    """Retrieve pending intakes for a specific compartment"""

    # Map compartment ID to the correct model
    compartment_models = {1: Compartment1, 2: Compartment2, 3: Compartment3}
    CompartmentModel = compartment_models.get(comp_id)

    if not CompartmentModel:
        return Response({"error": "Invalid compartment ID"}, status=status.HTTP_400_BAD_REQUEST)

    # Filter pending intakes by compartment
    pending_intakes = CompartmentIntake.objects.filter(
        compartment_type=ContentType.objects.get_for_model(CompartmentModel),
        taken=False
    ).order_by('intake_time')

    # Serialize and return the response
    serializer = CompartmentIntakeSerializer(pending_intakes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_taken_intakes_by_compartment(request, comp_id):
    """Retrieve taken intakes for a specific compartment"""

    # Map compartment ID to the correct model
    compartment_models = {1: Compartment1, 2: Compartment2, 3: Compartment3}
    CompartmentModel = compartment_models.get(comp_id)

    if not CompartmentModel:
        return Response({"error": "Invalid compartment ID"}, status=status.HTTP_400_BAD_REQUEST)

    # Filter taken intakes by compartment
    taken_intakes = CompartmentIntake.objects.filter(
        compartment_type=ContentType.objects.get_for_model(CompartmentModel),
        taken=True
    ).order_by('-taken_time')  # Order by most recent taken intake first

    # Serialize and return the response
    serializer = CompartmentIntakeSerializer(taken_intakes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
