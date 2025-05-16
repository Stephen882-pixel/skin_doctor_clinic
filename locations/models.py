from django.db import models

# Create your models here.

class Location(models.Model):
    """Model for clinic locations"""
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    latitude = models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    longitude = models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)

    def __str__(self):
        return self.name
    

class OperatingHours(models.Model):
    """Model for the clinic operating hours"""
    location =  models.ForeignKey(Location,on_delete=models.CASCADE,related_name='operating_hours')
    day_of_week = models.IntegerField(choices=[
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ])

    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('location','day_of_week')
        ordering = ['day_of_week']

    def __str__(self):
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if self.is_closed:
            return f"{self.location.name} - {day_names[self.day_of_week]} : Closed"
        return f"{self.location.name} {day_names[self.day_of_week]}: {self.opening_time} -  {self.closing_time}"
    