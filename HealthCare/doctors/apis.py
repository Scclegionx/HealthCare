from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Doctor
from .serializers import DoctorSerializer, DoctorLoginSerializer
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def register(request):
    try:
        print("Bắt đầu đăng ký bác sĩ...")
        data = request.POST if hasattr(request, 'POST') else request.data
        print("Dữ liệu nhận được:", data)
        
        serializer = DoctorSerializer(data=data)
        print("Serializer data:", serializer.initial_data)
        
        if serializer.is_valid():
            print("Dữ liệu hợp lệ:", serializer.validated_data)
            user = serializer.save()
            print("Tạo user thành công:", user.id)
            return Response({
                'message': 'Đăng ký thành công',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'specialization': user.specialization,
                    'license_number': user.license_number
                }
            }, status=status.HTTP_201_CREATED)
        print("Lỗi validate:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("Lỗi khi đăng ký:", str(e))
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login_api(request):
    serializer = DoctorLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password, using='default')
        if user is not None and isinstance(user, Doctor):
            login(request, user)
            return Response({'message': 'Đăng nhập thành công'}, status=status.HTTP_200_OK)
        return Response({'error': 'Tên đăng nhập hoặc mật khẩu không đúng'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 