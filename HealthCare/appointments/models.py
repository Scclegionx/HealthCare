from django.db import models

class Appointment(models.Model):
    doctor_id = models.IntegerField()  # ID của bác sĩ từ service doctors
    patient_id = models.IntegerField()  # ID của bệnh nhân từ service patients
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Chờ xác nhận'),
        ('scheduled', 'Đã sắp xếp lịch'),
        ('cancelled', 'Đã hủy')
    ], default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Appointment {self.id} - Doctor {self.doctor_id} - Patient {self.patient_id}"
