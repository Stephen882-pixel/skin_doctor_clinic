from  rest_framework import serializers
from .models import Feedback
from accounts.serializers import UserSerializer
from accounts.models import Doctor
from services.models import Service

class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for model field"""
    user_name = serializers.SerializerMethodField(read_only=True)
    doctor_name = serializers.SerializerMethodField(read_ony=True)
    service_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        moodel =Feedback
        fields = ['id', 'user', 'user_name', 'name', 'email', 'rating', 'comment', 
                  'doctor', 'doctor_name', 'service', 'service_name', 
                  'is_approved', 'created_at']
        extra_kwargs = {
            'user': {'read_only': True},
            'is_approved': {'read_only': True},
        }


    def get_user_name(self,obj):
        if obj.user:
            return obj.user.get_full_name() or obj.user.username
        return obj.name or "Anonymous"
    
    def get_doctor_name(self,obj):
        if obj.doctor:
            return f"Dr. {obj.doctor.user.get_full_name()}" if obj.doctor.user.get_full_name() else f"Dr. {obj.doctor.user.username}"
        return None
    
    def get_service_name(self,obj):
        if obj.service:
            return obj.service.name
        return None
    
    def create(self,validated_data):
        # set the user from the request if authenticated
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user

        # validate doctor and service
        doctor_id = self.initial_data.get('doctor')
        service_id = self.initial_data.get('service')

        if doctor_id:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                validated_data['doctor'] = doctor
            except Doctor.DoesNotExist:
                raise serializers.ValidationError({"doctor":"Doctor not found"})
        
        if service_id:
            try:
                service = Service.objects.get(id=service_id)
                validated_data['service'] = service
            except Service.DoesNotExist:
                raise serializers.ValidationError({"service":"Service not found"})
        
        return super().create(validated_data)
    
class FeedbackDetailSerializer(FeedbackSerializer):
    """Detailed serializer for feedback model"""
    user = UserSerializer(read_only=True)

    class Meta(FeedbackSerializer.Meta):
        fields = FeedbackSerializer.Meta.fields
        

                