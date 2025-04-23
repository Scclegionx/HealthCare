from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from .models import Doctor
from .serializers import DoctorSerializer, DoctorLoginSerializer
from . import apis
from django.contrib.auth.hashers import make_password
import requests
from django.conf import settings
from datetime import datetime

# Create your views here.

class DoctorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Doctor.objects.get(username=username)
            if user.check_password(password):
                return user
        except Doctor.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Doctor.objects.get(pk=user_id)
        except Doctor.DoesNotExist:
            return None

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = Doctor.objects.get(username=username)
            if user.check_password(password):
                login(request, user, backend='doctors.views.DoctorBackend')
                # Debug
                print(f"User authenticated: {request.user.is_authenticated}")
                print(f"User type: {type(request.user)}")
                return redirect('/doctors/home/')
            else:
                messages.error(request, 'Mật khẩu không đúng')
        except Doctor.DoesNotExist:
            messages.error(request, 'Tên đăng nhập không tồn tại')
    
    return render(request, 'doctors/login.html')

def register_page(request):
    if request.method == 'POST':
        print("Dữ liệu POST nhận được:", request.POST)
        response = apis.register(request)
        print("Response từ API:", response.data)
        if response.status_code == 201:
            messages.success(request, 'Đăng ký thành công')
            return redirect('doctors:login')
        # Xử lý lỗi cụ thể
        if 'license_number' in response.data:
            messages.error(request, 'Số giấy phép hành nghề đã tồn tại. Vui lòng kiểm tra lại.')
        else:
            messages.error(request, response.data.get('error', 'Có lỗi xảy ra'))
    return render(request, 'doctors/register.html')

@login_required(login_url='/doctors/login/')
def home(request):
    # Debug
    print(f"Home - User authenticated: {request.user.is_authenticated}")
    print(f"Home - User type: {type(request.user)}")
    
    if not isinstance(request.user, Doctor):
        logout(request)
        return redirect('/doctors/login/')
    return render(request, 'doctors/home.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def list_appointments(request):
    if not request.user.is_doctor:
        messages.error(request, "Bạn không có quyền truy cập trang này!")
        return redirect('home')
    try:
        response = requests.get(
            f"{settings.BASE_URL}/appointments/api/appointments/doctor/{request.user.id}/"
        )
        appointments = response.json()
        print(f"Appointments: {appointments}")
    except Exception as e:
        appointments = []
        messages.error(request, "Có lỗi xảy ra khi tải danh sách lịch hẹn!")
    
    return render(request, 'doctors/list_appointments.html', {
        'appointments': appointments
    })

@login_required
def schedule_appointments(request):
    if not request.user.is_doctor:
        messages.error(request, "Bạn không có quyền truy cập trang này!")
        return redirect('home')
    
    try:
        response = requests.get(
            f"{settings.BASE_URL}/appointments/api/appointments/pending/{request.user.id}/"
        )
        pending_appointments = response.json()
    except Exception as e:
        pending_appointments = []
        messages.error(request, "Có lỗi xảy ra khi tải danh sách lịch hẹn chờ!")
    
    return render(request, 'doctors/schedule_appointments.html', {
        'pending_appointments': pending_appointments
    })

@login_required
def save_schedule(request, appointment_id):
    if not request.user.is_doctor:
        messages.error(request, "Bạn không có quyền thực hiện thao tác này!")
        return redirect('home')
    
    if request.method == 'POST':
        # Get form data
        date = request.POST.get('date')
        start_hour = request.POST.get('start_hour')
        start_minute = request.POST.get('start_minute')
        end_hour = request.POST.get('end_hour')
        end_minute = request.POST.get('end_minute')
        
        # Construct datetime strings
        start_time = f"{date}T{start_hour}:{start_minute}:00"
        end_time = f"{date}T{end_hour}:{end_minute}:00"
        
        # print("Form data:")
        # print(f"Date: {date}")
        # print(f"Start Hour: {start_hour}")
        # print(f"Start Minute: {start_minute}")
        # print(f"End Hour: {end_hour}")
        # print(f"End Minute: {end_minute}")
        # print(f"Start Time: {start_time}")
        # print(f"End Time: {end_time}")
        
        try:
            response = requests.post(
                f"{settings.BASE_URL}/appointments/api/appointments/schedule/",
                json={
                    'appointment_id': appointment_id,
                    'start_time': start_time,
                    'end_time': end_time
                }
            )
            
            # print(f"API Response: {response.status_code}")
            # print(f"API Response Data: {response.text}")
            
            if response.status_code == 200:
                messages.success(request, "Đã sắp xếp lịch hẹn thành công!")
            else:
                error_message = response.json().get('error', 'Có lỗi xảy ra khi sắp xếp lịch hẹn!')
                messages.error(request, error_message)
                
        except Exception as e:
            print(f"Error: {str(e)}")
            messages.error(request, f"Có lỗi xảy ra khi kết nối với server: {str(e)}")
            
    return redirect('doctors:schedule_appointments')
