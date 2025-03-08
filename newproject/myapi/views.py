from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer, MedicineSerializer, CompartmentIntakeSerializer
from .models import User, Compartment1, CompartmentIntake
from datetime import datetime
from django.utils.timezone import localtime
from django.utils.timezone import now


@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)#rispondi con un json
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ✅ Get all medicines
@api_view(['GET'])
def get_medicines(request):
    medicines = Compartment1.objects.all()
    serializer = MedicineSerializer(medicines, many=True)
    return Response(serializer.data)

# ✅ Create a new medicine entry (with validation from model)
@api_view(['POST'])
def create_medicine(request):
    serializer = MedicineSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get, Update, or Delete a specific medicine entry
@api_view(['GET', 'PUT', 'DELETE'])
def medicine_detail(request, pk):
    medicine = get_object_or_404(Compartment1, pk=pk)

    if request.method == 'GET':
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MedicineSerializer(medicine, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()  # Triggers validation
                return Response(serializer.data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        medicine.delete()
        return Response({"message": "Medicine deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
def get_daily_schedule(request):
    """Retrieve all medicines that should be taken today"""
    
    # Get current time (localized)
    now = localtime().time()

    # Fetch repeated medicines with at least one valid time set
    repeated_medicines = Compartment1.objects.filter(
        to_be_repeated=True
    ).exclude(orario_mattina=None, orario_pomeriggio=None, orario_sera=None)

    # Fetch non-repeated medicines that have a set time
    one_time_medicines = Compartment1.objects.filter(
        to_be_repeated=False
    ).exclude(orario_medicina=None)

    # Serialize the results
    repeated_serializer = MedicineSerializer(repeated_medicines, many=True)
    one_time_serializer = MedicineSerializer(one_time_medicines, many=True)

    return Response({
        "repeated_medicines": repeated_serializer.data,
        "one_time_medicines": one_time_serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def mark_intake_as_taken(request, intake_id):
    """Marks a specific intake instance as taken"""
    intake = get_object_or_404(CompartmentIntake, id=intake_id)

    if intake.taken:
        return Response({"message": "This dose has already been taken."}, status=status.HTTP_400_BAD_REQUEST)

    intake.mark_as_taken()
    serializer = CompartmentIntakeSerializer(intake)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
def get_pending_intakes(request):
    """Retrieve all pending medicine intakes"""
    pending_intakes = CompartmentIntake.objects.filter(taken=False).order_by('intake_time')
    serializer = CompartmentIntakeSerializer(pending_intakes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_taken_intakes(request):
    """Retrieve all medicines that have been taken with their timestamps"""
    taken_intakes = CompartmentIntake.objects.filter(taken=True).order_by('-taken_time')
    serializer = CompartmentIntakeSerializer(taken_intakes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
