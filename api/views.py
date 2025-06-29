from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import (
    UserSerializer, 
    UserCreateSerializer, 
    UserUpdateSerializer
)
from utils.decorators import measure_time


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели User с полным CRUD функционалом
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """Настройка разрешений для разных действий"""
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
    @measure_time
    def list(self, request, *args, **kwargs):
        """Список пользователей с измерением времени выполнения"""
        return super().list(request, *args, **kwargs)
    
    @measure_time
    def retrieve(self, request, *args, **kwargs):
        """Получение пользователя по ID с измерением времени"""
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Получение информации о текущем пользователе"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Верификация пользователя"""
        user = self.get_object()
        user.is_verified = True
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Аутентификация пользователя"""
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Необходимо указать username и password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        if user:
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Неверные учетные данные'},
                status=status.HTTP_401_UNAUTHORIZED
            )
