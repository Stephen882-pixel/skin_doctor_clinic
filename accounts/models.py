from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.

class User(AbstractUser):
    """"Custom user model for all users in the system"""
    USER_TYPE_CHOICE = (
        ('patient','Patient'),
        ('doctor','Doctor'),
        ('admin','Admin'),
    )

    email = models.EmailField(_('email address'),unique=True)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',blank=True,null=True)
    user_type = models.CharField(max_length=10,choices=USER_TYPE_CHOICE,default='patient')
    date_of_birth = models.DateTimeField(blank=True,null=True)
    address = models.TextField(blank=True,null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    

class Doctor(models.Model):
    """Model for Doctor profiles"""
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='doctor_profile')
    specialization = models.CharField(max_length=100)
    qualifications = models.TextField()
    experience_years = models.PositiveIntegerField(default=0)
    bio = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'Dr. {self.user.get_full_name}'
    

class Patient(models.Model):
    """Model for patient profiles"""
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='patient_profile')
    medical_history = models.TextField(blank=True,null=True)
    allergies = models.TextField(blank=True,null=True)
    emergency_contact_name = models.CharField(max_length=100,blank=True,null=True)
    emergency_contact_number = models.CharField(max_length=15,blank=True,null=True)


    def __str__(self):
        return f'Patient: {self.user.get_full_name}'
    

