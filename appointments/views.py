from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from accounts.permissions import IsAdminUser, IsOwnerOrAdmin
from .models import Appointment, DoctorSchedule, DoctorTimeOff
from .serializers import (
    AppointmentSerializer, AppointmentDetailSerializer, 
    DoctorScheduleSerializer, DoctorTimeOffSerializer,
    AppointmentCreateSerializer
)
from accounts.models import Doctor, Patient

class AppointmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Appointment model"""
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return AppointmentDetailSerializer
        elif self.action == 'create':
            return AppointmentCreateSerializer
        return AppointmentSerializer
    
    def get_queryset(self):
        """
        Customize queryset based on user role:
        - Admins see all appointments
        - Doctors see their own appointments
        - Patients see their own appointments
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.is_staff:  # Admin sees all
            return queryset
        
        # Doctor sees their appointments
        if hasattr(user, 'doctor_profile'):
            return queryset.filter(doctor=user.doctor_profile)
        
        # Patient sees their appointments
        if hasattr(user, 'patient_profile'):
            return queryset.filter(patient=user.patient_profile)
        
        # Other users see nothing
        return Appointment.objects.none()
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """Set patient automatically for patient users"""
        if not self.request.user.is_staff and hasattr(self.request.user, 'patient_profile'):
            serializer.save(patient=self.request.user.patient_profile)
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_appointments(self, request):
        """Get current user's appointments"""
        user = request.user
        
        if hasattr(user, 'doctor_profile'):
            appointments = Appointment.objects.filter(doctor=user.doctor_profile)
        elif hasattr(user, 'patient_profile'):
            appointments = Appointment.objects.filter(patient=user.patient_profile)
        else:
            return Response(
                {"detail": "You don't have any appointments."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AppointmentDetailSerializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        """Cancel an appointment"""
        appointment = self.get_object()
        
        # Check if user has permission to cancel
        user = request.user
        if not user.is_staff and not (
            (hasattr(user, 'doctor_profile') and appointment.doctor == user.doctor_profile) or
            (hasattr(user, 'patient_profile') and appointment.patient == user.patient_profile)
        ):
            return Response(
                {"detail": "You don't have permission to cancel this appointment."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if appointment.status == 'canceled':
            return Response(
                {"detail": "This appointment is already canceled."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment.status = 'canceled'
        appointment.save()
        
        return Response(
            {"detail": "Appointment canceled successfully."},
            status=status.HTTP_200_OK
        )

class DoctorScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet for DoctorSchedule model"""
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter schedules by doctor if specified in query params
        """
        queryset = super().get_queryset()
        doctor_id = self.request.query_params.get('doctor_id', None)
        
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_schedule(self, request):
        """Get current doctor's schedule"""
        user = request.user
        
        if not hasattr(user, 'doctor_profile'):
            return Response(
                {"detail": "You don't have a doctor profile."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        schedules = DoctorSchedule.objects.filter(doctor=user.doctor_profile)
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)

class DoctorTimeOffViewSet(viewsets.ModelViewSet):
    """ViewSet for DoctorTimeOff model"""
    queryset = DoctorTimeOff.objects.all()
    serializer_class = DoctorTimeOffSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter time offs by doctor if specified in query params
        """
        queryset = super().get_queryset()
        doctor_id = self.request.query_params.get('doctor_id', None)
        
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """Set doctor automatically for doctor users"""
        if hasattr(self.request.user, 'doctor_profile'):
            serializer.save(doctor=self.request.user.doctor_profile)
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_time_offs(self, request):
        """Get current doctor's time offs"""
        user = request.user
        
        if not hasattr(user, 'doctor_profile'):
            return Response(
                {"detail": "You don't have a doctor profile."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        time_offs = DoctorTimeOff.objects.filter(doctor=user.doctor_profile)
        serializer = self.get_serializer(time_offs, many=True)
        return Response(serializer.data)