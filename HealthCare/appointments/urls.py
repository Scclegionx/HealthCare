from django.urls import path
from . import apis

app_name = 'appointments'

urlpatterns = [
    path('api/appointments/doctor/<int:doctor_id>/', apis.get_doctor_appointments, name='api_doctor_appointments'),
    path('api/appointments/pending/<int:doctor_id>/', apis.get_pending_appointments, name='api_pending_appointments'),
    path('api/appointments/schedule/', apis.schedule_appointment, name='api_schedule_appointment'),
    path('api/appointments/request/', apis.create_appointment_request, name='api_create_appointment'),
]
