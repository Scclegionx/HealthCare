from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'date_of_birth', 'phone_number', 'address']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Mật khẩu không khớp")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = Patient.objects.create_user(**validated_data)
        return user

class PatientLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True) 