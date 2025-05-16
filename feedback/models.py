from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from accounts.models import User,Doctor
from services.models import Service

# Create your models here.
class Feedback(models.Model):
    """Model for feedback from users"""
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='feedback')
    name = models.CharField(max_length=100,blank=True,null=True,help_text="For anonymous feedback")
    email =  models.EmailField(blank=True,null=True,help_text="For anonymous feedback")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.TextField()
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True,blank=True,related_name='feedback')
    service = models.ForeignKey(Service,on_delete=models.CASCADE,null=True,blank=True,related_name='feedback')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.user:
            return f'Feedback from {self.user.get_full_name()} - Rating:{self.rating}'
        return f"Anonymous feedback - Rating: {self.rating}"
    
