from django.db import models
from django.contrib.auth.models import AbstractUser

class Doctor(AbstractUser):
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.IntegerField(default=0)
    hospital = models.CharField(max_length=200, null=True, blank=True)

    # Thêm related_name cho groups và user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='doctor_set',
        blank=True,
        help_text='The groups this doctor belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='doctor_set',
        blank=True,
        help_text='Specific permissions for this doctor.',
        verbose_name='user permissions',
    )

    @property
    def is_doctor(self):
        return True

    class Meta:
        verbose_name = 'Bác sĩ'
        verbose_name_plural = 'Bác sĩ'
        db_table = 'doctors'  # Tên bảng trong MySQL
        app_label = 'doctors'  # Chỉ định app label

    def __str__(self):
        return f"Bác sĩ {self.username}"

    def save(self, *args, **kwargs):
        # Không cần truyền using ở đây vì đã được xử lý trong router
        super().save(*args, **kwargs)
