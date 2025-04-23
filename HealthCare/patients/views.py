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
