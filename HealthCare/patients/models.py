from django.db import models
from django.contrib.auth.models import AbstractUser

class Patient(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    # Thêm related_name cho groups và user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='patient_set',
        blank=True,
        help_text='The groups this patient belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='patient_set',
        blank=True,
        help_text='Specific permissions for this patient.',
        verbose_name='user permissions',
    )

    class Meta:
        verbose_name = 'Bệnh nhân'
        verbose_name_plural = 'Bệnh nhân'
        db_table = 'patients'  # Tên bảng trong MySQL
        app_label = 'patients'  # Chỉ định app label

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Không cần truyền using ở đây vì đã được xử lý trong router
        super().save(*args, **kwargs)
