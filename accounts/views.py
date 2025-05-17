from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Doctor, Patient
from .serializers import (
    UserSerializer, DoctorSerializer, PatientSerializer,
    DoctorRegistrationSerializer, PatientRegistrationSerializer
)
from .permissions import IsAdminUser, IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get the current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_me(self, request):
        """Update the current user profile"""
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class DoctorViewSet(viewsets.ModelViewSet):
    """Viewset for doctor model"""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get the current doctor's profile"""
        try:
            doctor = Doctor.objects.get(user=request.user)
            serializer = self.get_serializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response({
                "detail": "You do not have a doctor profile."
            }, status=status.HTTP_404_NOT_FOUND)
        
class PatientViewSet(viewsets.ModelViewSet):
    """Viewset for patient model"""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]
        elif self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return [IsOwnerOrAdmin()]
        elif self.action == 'list':
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get the current patient's profile"""
        try:
            patient = Patient.objects.get(user=request.user)
            serializer = self.get_serializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response(
                {"detail": "You do not have a patient profile."},
                status=status.HTTP_404_NOT_FOUND
            )

class DoctorRegistrationView(generics.CreateAPIView):
    """View for registering a new doctor"""
    serializer_class = DoctorRegistrationSerializer
    permission_classes = [IsAdminUser]

class PatientRegistrationView(generics.CreateAPIView):
    """View for registering a new patient"""
    serializer_class = PatientRegistrationSerializer
    permission_classes = [IsAuthenticated]