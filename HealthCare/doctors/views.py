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
