from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Patient
from .serializers import PatientSerializer, PatientLoginSerializer
from . import apis
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
import requests
from django.conf import settings

# Create your views here.

class PatientBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Patient.objects.get(email=email)
            if user.check_password(password):
                return user
        except Patient.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Patient.objects.get(pk=user_id)
        except Patient.DoesNotExist:
            return None

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = Patient.objects.get(email=email)
            if user.check_password(password):
                login(request, user, backend='patients.views.PatientBackend')
                print(f"User authenticated: {request.user.is_authenticated}")
                print(f"User type: {type(request.user)}")
                return redirect('patients:home')
            else:
                messages.error(request, 'Mật khẩu không đúng')
        except Patient.DoesNotExist:
            messages.error(request, 'Email không tồn tại')
    
    return render(request, 'patients/login.html')

def register_page(request):
    if request.method == 'POST':
        response = apis.register(request)
        if response.status_code == 201:
            return redirect('patients:login')
        return render(request, 'patients/register.html', {'error': response.data})
    return render(request, 'patients/register.html')

@login_required
def home(request):
    if not isinstance(request.user, Patient):
        return redirect('login')
    return render(request, 'patients/home.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def list_doctors(request):
    
    try:
        # Gọi API lấy danh sách bác sĩ
        response = requests.get(f"{settings.BASE_URL}/doctors/api/doctors/")
        doctors = response.json()
    except Exception as e:
        doctors = []
        messages.error(request, "Có lỗi xảy ra khi tải danh sách bác sĩ!")
    
    return render(request, 'patients/list_doctor.html', {
        'doctors': doctors
    })

@login_required
def make_appointment(request, doctor_id):
    
    if request.method == 'POST':
        try:
            # Sửa lại URL endpoint
            response = requests.post(
                f"{settings.BASE_URL}/appointments/api/appointments/request/",
                json={
                    'doctor_id': doctor_id,
                    'patient_id': request.user.id
                }
            )
            
            if response.status_code == 201:
                messages.success(request, "Đã đặt lịch khám thành công! Vui lòng chờ bác sĩ xác nhận.")
            else:
                error_data = response.json()
                error_message = error_data.get('error', "Có lỗi xảy ra khi đặt lịch khám!")
                messages.error(request, error_message)
                
        except Exception as e:
            messages.error(request, f"Có lỗi xảy ra khi kết nối với server: {str(e)}")
    
    return redirect('patients:list_doctors')
