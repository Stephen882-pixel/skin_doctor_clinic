from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Doctor,Patient

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User Model"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','email','username','first_name','last_name',
                  'phone_number','profile_picture','user_type','date_of_birth','address']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self,instance,validated_data):
        password = validated_data.pop('password',None)
        user = super().update(instance,validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only = True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'user_id', 'specialization', 'qualifications', 
                  'experience_years', 'bio', 'is_available', 'full_name']
        
    def get_full_name(self,obj):
        return f'Dr. {obj.user.get_full_name()}' if obj.user.get_full_name()  else f"Dr. {obj.user.username}"
    
class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Patient
        fields = ['id', 'user', 'user_id', 'medical_history', 'allergies', 
                  'emergency_contact_name', 'emergency_contact_number']

class DoctorRegistrationSerializer(serializers.Serializer):
    """Serializer for registering a new doctor with user details"""
    # User fields
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=15, required=False)
    profile_picture = serializers.ImageField(required=False)
    date_of_birth = serializers.DateField(required=False)
    address = serializers.CharField(required=False)
    
    # Doctor fields
    specialization = serializers.CharField(max_length=100)
    qualifications = serializers.CharField()
    experience_years = serializers.IntegerField(min_value=0)
    bio = serializers.CharField()
    
    def create(self, validated_data):
        # Extract doctor fields
        doctor_data = {
            'specialization': validated_data.pop('specialization'),
            'qualifications': validated_data.pop('qualifications'),
            'experience_years': validated_data.pop('experience_years'),
            'bio': validated_data.pop('bio'),
        }
        
        # Create user
        validated_data['user_type'] = 'doctor'
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create doctor profile
        doctor = Doctor.objects.create(user=user, **doctor_data)
        
        return doctor


class PatientRegistrationSerializer(serializers.Serializer):
    """Serializer for registering a new patient with user details"""
    # User fields
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=15, required=False)
    profile_picture = serializers.ImageField(required=False)
    date_of_birth = serializers.DateField(required=False)
    address = serializers.CharField(required=False)
    
    # Patient fields
    medical_history = serializers.CharField(required=False)
    allergies = serializers.CharField(required=False)
    emergency_contact_name = serializers.CharField(max_length=100, required=False)
    emergency_contact_number = serializers.CharField(max_length=15, required=False)
    
    def create(self, validated_data):
        # Extract patient fields
        patient_data = {
            'medical_history': validated_data.pop('medical_history', None),
            'allergies': validated_data.pop('allergies', None),
            'emergency_contact_name': validated_data.pop('emergency_contact_name', None),
            'emergency_contact_number': validated_data.pop('emergency_contact_number', None),
        }
        
        # Create user
        validated_data['user_type'] = 'patient'
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create patient profile
        patient = Patient.objects.create(user=user, **patient_data)
        
        return patient