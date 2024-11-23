from rest_framework import serializers
from .models import Shop, ShopHours

class ShopHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopHours
        fields = ['id', 'day', 'opening_time', 'closing_time', 'is_closed']

class ShopSerializer(serializers.ModelSerializer):
    hours = ShopHoursSerializer(many=True, read_only=True)
    
    class Meta:
        model = Shop
        fields = [
            'id', 'name', 'slug', 'description', 'logo', 
            'banner', 'address', 'phone', 'email', 
            'is_active', 'rating', 'review_count', 
            'hours', 'created_at', 'updated_at'
        ]
        read_only_fields = ['rating', 'review_count']