from rest_framework import serializers
from .models import Doctor
from django.contrib.auth.hashers import make_password

class DoctorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'specialization', 'license_number', 'years_of_experience', 'hospital']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        print("Validating data:", data)
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Mật khẩu không khớp")
        return data

    def create(self, validated_data):
        print("Creating user with data:", validated_data)
        validated_data.pop('confirm_password')
        user = Doctor.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            specialization=validated_data['specialization'],
            license_number=validated_data['license_number'],
            years_of_experience=validated_data.get('years_of_experience', 0),
            hospital=validated_data.get('hospital')
        )
        print("User created:", user.id)
        return user

class DoctorLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True) 