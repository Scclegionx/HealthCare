from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer
from datetime import datetime
import requests
from django.conf import settings

def get_doctor_info(doctor_id):
    try:
        response = requests.get(f"{settings.BASE_URL}/doctors/api/doctors/{doctor_id}/")
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None

def get_patient_info(patient_id):
    try:
        response = requests.get(f"{settings.BASE_URL}/patients/api/patients/{patient_id}/")
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None

def enrich_appointment_data(appointment):
    """Thêm thông tin bác sĩ và bệnh nhân vào appointment"""
    doctor_info = get_doctor_info(appointment.doctor_id)
    patient_info = get_patient_info(appointment.patient_id)
    
    return {
        'id': appointment.id,
        'doctor_id': appointment.doctor_id,
        'patient_id': appointment.patient_id,
        'doctor_name': doctor_info.get('full_name') if doctor_info else 'Unknown Doctor',
        'patient_name': patient_info.get('full_name') if patient_info else 'Unknown Patient',
        'start_time': appointment.start_time,
        'end_time': appointment.end_time,
        'status': appointment.status,
        'created_at': appointment.created_at
    }

@api_view(['GET'])
def get_doctor_appointments(request, doctor_id):
    try:
        appointments = Appointment.objects.filter(
            doctor_id=doctor_id,
            status='scheduled',
            start_time__date=datetime.now().date()
        )
        
        # Enrich data with doctor and patient information
        enriched_appointments = [
            enrich_appointment_data(appointment) 
            for appointment in appointments
        ]
        
        return Response(enriched_appointments)
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_pending_appointments(request, doctor_id):
    try:
        appointments = Appointment.objects.filter(
            doctor_id=doctor_id,
            status='pending'
        )
        
        # Enrich data with doctor and patient information
        enriched_appointments = [
            enrich_appointment_data(appointment) 
            for appointment in appointments
        ]
        
        return Response(enriched_appointments)
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def schedule_appointment(request):
    try:
        appointment_id = request.data.get('appointment_id')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        appointment = Appointment.objects.get(id=appointment_id)
        appointment.start_time = start_time
        appointment.end_time = end_time
        appointment.status = 'scheduled'
        appointment.save()

        return Response(enrich_appointment_data(appointment))
    except Appointment.DoesNotExist:
        return Response(
            {"error": "Appointment not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def create_appointment_request(request):
    try:
        doctor_id = request.data.get('doctor_id')
        patient_id = request.data.get('patient_id')

        # Verify doctor exists
        doctor_info = get_doctor_info(doctor_id)
        if not doctor_info:
            return Response(
                {"error": "Doctor not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Verify patient exists
        patient_info = get_patient_info(patient_id)
        if not patient_info:
            return Response(
                {"error": "Patient not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        appointment = Appointment.objects.create(
            doctor_id=doctor_id,
            patient_id=patient_id,
            status='pending'
        )
        
        return Response(
            enrich_appointment_data(appointment), 
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 