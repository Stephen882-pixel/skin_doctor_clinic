from rest_framework import serializers

from accounts import models
from .models import Appointment,DoctorSchedule,DoctorTimeOff
from accounts.serializers import DoctorSerializer,PatientSerializer
from services.serializers import ServiceSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    """serializer for appointmen model"""
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor',read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(source='patient',read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(source='service',read_only=True)


    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'doctor_id', 'patient', 'patient_id', 'service', 'service_id',
                  'date', 'start_time', 'end_time', 'status', 'notes', 'created_at', 'updated_at']
        extra_kwargs = {
            'doctor': {'write_only': True},
            'patient': {'write_only': True},
            'service': {'write_only': True},
        }

class AppointmentDetailSerializer(AppointmentSerializer):
    """Detailed serializer for Appointment model with related objects"""
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)


    class Meta(AppointmentSerializer.Meta):
        fields = AppointmentSerializer.Meta.fields


class DoctorScheduleSerializer(serializers.ModelSerializer):
    """Serializer for DoctorSchedule model"""
    day_name = serializers.SerializerMethodField()

    class Meta:
        model = DoctorSchedule
        fields = ['id', 'doctor', 'day_of_week', 'day_name', 'start_time', 'end_time', 'is_available']
    
    def get_day_name(self, obj):
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return day_names[obj.day_of_week]
    

class DoctorTimeOffSerializer(serializers.ModelSerializer):
    """Serializer for DoctorTimeOff model"""
    class Meta:
        model = DoctorTimeOff
        fields = ['id', 'doctor', 'start_datetime', 'end_datetime', 'reason']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new appointment"""
    
    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'service', 'date', 'start_time', 'end_time', 'notes']
    
    def validate(self, data):
        """
        Validate that the appointment doesn't conflict with existing appointments
        and is within doctor's schedule
        """
        doctor = data['doctor']
        date = data['date']
        start_time = data['start_time']
        end_time = data['end_time']
        
        # Check if appointment time is valid (end time after start time)
        if end_time <= start_time:
            raise serializers.ValidationError("End time must be after start time")
        
        # Check if date is a day the doctor works
        day_of_week = date.weekday()  # 0 for Monday, 6 for Sunday
        try:
            schedule = DoctorSchedule.objects.get(doctor=doctor, day_of_week=day_of_week)
            if not schedule.is_available:
                raise serializers.ValidationError("Doctor is not available on this day")
            
            # Check if appointment is within working hours
            if start_time < schedule.start_time or end_time > schedule.end_time:
                raise serializers.ValidationError("Appointment is outside doctor's working hours")
        except DoctorSchedule.DoesNotExist:
            raise serializers.ValidationError("Doctor does not work on this day")
        
        # Check for doctor time off
        time_offs = DoctorTimeOff.objects.filter(
            doctor=doctor,
            start_datetime__lte=f"{date} {end_time}",
            end_datetime__gte=f"{date} {start_time}"
        )
        if time_offs.exists():
            raise serializers.ValidationError("Doctor is on time off during this period")
        
        # Check for conflicting appointments
        conflicting_appointments = Appointment.objects.filter(
            doctor=doctor,
            date=date,
            status__in=['pending', 'confirmed'],
        ).filter(
            # Appointment starts or ends during existing appointment
            (models.Q(start_time__lt=end_time) & models.Q(end_time__gt=start_time))
        )
        
        if self.instance:  # If updating an existing appointment
            conflicting_appointments = conflicting_appointments.exclude(id=self.instance.id)
        
        if conflicting_appointments.exists():
            raise serializers.ValidationError("This time slot conflicts with an existing appointment")
        
        return data