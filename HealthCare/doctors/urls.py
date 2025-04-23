from django.urls import path
from . import views, apis

app_name = 'doctors'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('appointments/', views.list_appointments, name='list_appointments'),
    path('appointments/schedule/', views.schedule_appointments, name='schedule_appointments'),
    path('appointments/schedule/<int:appointment_id>/save/', views.save_schedule, name='save_schedule'),
    path('api/doctors/<int:doctor_id>/', apis.get_doctor_info, name='api_doctor_info'),
] 