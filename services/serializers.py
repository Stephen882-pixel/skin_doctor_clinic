from rest_framework import serializers
from .models import ServiceCategory,Service

class ServiceCategorySerializer(serializers.ModelSerializer):
    """Serializer for servicecategory model"""
    class Meta:
        model = ServiceCategory
        fields = ['id','name','description','image']

class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for service model"""
    category_name = serializers.CharField(source='category.name',read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'duration', 'price', 'image', 
                  'category', 'category_name', 'is_active', 'created_at', 'updated_at']
        
class ServiceDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for service model with category details"""
    category = ServiceCategorySerializer(read_only=True)

    class Meta:
        fields = ServiceSerializer.Meta.fields
        