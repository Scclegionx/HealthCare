from django.db import models
from django.contrib.auth.models import AbstractUser

class Doctor(AbstractUser):
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.IntegerField(default=0)
    hospital = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Bác sĩ'
        verbose_name_plural = 'Bác sĩ'
        db_table = 'doctors'  # Tên bảng trong MySQL
        app_label = 'doctors'  # Chỉ định app label

    def __str__(self):
        return f"Bác sĩ {self.username}"

    def save(self, *args, **kwargs):
        # Đảm bảo lưu vào MySQL
        super().save(using='mysql', *args, **kwargs)
