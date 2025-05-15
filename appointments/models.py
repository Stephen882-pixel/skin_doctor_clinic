from django.db import models
from accounts.models import Doctor,Patient
from services.models import Service


# Create your models here.
class Appointment(models.Model):
    """Model for appointment between doctors and patients"""
    STATUS_CHOICES = (
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('completed','Completed'),
        ('canceled','Canceled'),
    )

    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='appointments')
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='appoitments')
    service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name='appointments')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')
    notes = models.CharField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date','-start_time']

    def __str__(self):
        return f'{self.patient} - {self.service} - {self.date} {self.start_time}'
    
class DoctorSchedule(models.Model):
    """Model for doctor's working schedule"""
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='schedules')
    day_of_the_week = models.IntegerField(choices=[
        (0,'Monday'),
        (1,'Tuesday'),
        (2,'Wednesday'),
        (3,'Thursday'),
        (4,'Friday'),
        (5,'Saturday'),
        (6,'Sunday'),

    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor','day_of_the_week')
        ordering = ['day_of_the_week','start_time']


    def __str__(self):
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return f'{self.doctor} - {day_names[self.day_of_the_week]} {self.start_time} - {self.end_time}'
    


class DoctorTimeOff(models.Model):
    """Model for doctor's time off"""
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='time_offs')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reason = models.CharField(max_length=255,blank=True,null=True)


    class Meta:
         ordering = ['-start_datetime']

    def __str__(self):
        return f'{self.doctor} - {self.start_datetime}'
    
    
        
    