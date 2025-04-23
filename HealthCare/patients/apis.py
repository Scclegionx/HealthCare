from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer, PatientLoginSerializer
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def register(request):
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        # Tạo user mới
        user = Patient.objects.using('default').create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=make_password(serializer.validated_data['password']),
            date_of_birth=serializer.validated_data.get('date_of_birth'),
            phone_number=serializer.validated_data.get('phone_number'),
            address=serializer.validated_data.get('address')
        )
        return Response({'message': 'Đăng ký thành công'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_api(request):
    serializer = PatientLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password, using='default')
        if user is not None and isinstance(user, Patient):
            login(request, user)
            return Response({'message': 'Đăng nhập thành công'}, status=status.HTTP_200_OK)
        return Response({'error': 'Tên đăng nhập hoặc mật khẩu không đúng'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_patient_info(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
        return Response({
            'id': patient.id,
            'full_name': f"{patient.first_name} {patient.last_name}",
            'username': patient.username,
            'email': patient.email,
            'phone': patient.phone  # giả sử có trường này
        })
    except Patient.DoesNotExist:
        return Response(
            {"error": "Patient not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 