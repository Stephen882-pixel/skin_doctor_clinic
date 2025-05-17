from rest_framework import serializers
from .models import Location,OperatingHours

class OperatingHoursSerializer(serializers.ModelSerializer):
    """Serializers for Operating hours model"""
    day_name = serializers.SerializerMethodField()

    class Meta:
        model = OperatingHours
        fields = ['id', 'location', 'day_of_week', 'day_name', 'opening_time', 'closing_time', 'is_closed']
    
    def get_day_name(self,obj):
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return day_names[obj.day_of_week]
    
class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location model"""
    class Meta:
        model = Location
        fields = ['id', 'name', 'address', 'city', 'state', 'zip_code', 'country',
                  'phone', 'email', 'latitude', 'longitude', 'is_active']

class LocationDetailSerializer(LocationSerializer):
    """Detailed serializer for Location model with operating hours"""
    operating_hours = OperatingHoursSerializer(many=True, read_only=True)
    
    class Meta(LocationSerializer.Meta):
        fields = LocationSerializer.Meta.fields + ['operating_hours']
        