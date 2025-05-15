from django.db import models


# Create your models here.

class ServiceCategory(models.Model):
    """Model for categorizing services"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='service_categories/',blank=True,null=True)

    class Meta:
        verbose_name_plural = "Service Categories"

    def _str__(self):
        return self.name
    
class Service(models.Model):
    """Model for services offered by the clinic"""
    name = models.CharField(max_length=100)
    descripition = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='service/',blank=True,null=True)
    category = models.ForeignKey(ServiceCategory,on_delete=models.CASCADE,related_name='services')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
    