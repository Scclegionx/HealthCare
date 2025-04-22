from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor

class MultiUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Thử đăng nhập với Patient
        try:
            user = Patient.objects.get(username=username)
            if user.check_password(password):
                return user
        except Patient.DoesNotExist:
            pass

        # Thử đăng nhập với Doctor
        try:
            user = Doctor.objects.get(username=username)
            if user.check_password(password):
                return user
        except Doctor.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        # Thử lấy Patient
        try:
            return Patient.objects.get(pk=user_id)
        except Patient.DoesNotExist:
            pass

        # Thử lấy Doctor
        try:
            return Doctor.objects.get(pk=user_id)
        except Doctor.DoesNotExist:
            pass

        return None 