from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer, PatientLoginSerializer

# Create your views here.

@api_view(['POST'])
def register(request):
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        # Sử dụng database mysql
        user = Patient.objects.using('mysql').create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            date_of_birth=serializer.validated_data.get('date_of_birth'),
            phone_number=serializer.validated_data.get('phone_number'),
            address=serializer.validated_data.get('address')
        )
        return Response({'message': 'Đăng ký thành công'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    serializer = PatientLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        # Sử dụng database mysql để xác thực
        user = authenticate(request, username=username, password=password)
        if user is not None and isinstance(user, Patient):
            login(request, user)
            return Response({'message': 'Đăng nhập thành công'}, status=status.HTTP_200_OK)
        return Response({'error': 'Tên đăng nhập hoặc mật khẩu không đúng'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def home(request):
    if not isinstance(request.user, Patient):
        return redirect('login')
    return render(request, 'patients/home.html', {'user': request.user})
