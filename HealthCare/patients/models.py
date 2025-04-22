from django.db import models
from django.contrib.auth.models import AbstractUser

class Patient(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Bệnh nhân'
        verbose_name_plural = 'Bệnh nhân'
        db_table = 'patients'  # Tên bảng trong MySQL
        app_label = 'patients'  # Chỉ định app label

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Đảm bảo lưu vào MySQL
        super().save(using='mysql', *args, **kwargs)
