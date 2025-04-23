from django.urls import path
from . import views, apis

app_name = 'patients'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('api/patients/<int:patient_id>/', apis.get_patient_info, name='api_patient_info'),
] 