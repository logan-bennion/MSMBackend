from rest_framework import serializers
from .models import ProductReview, ShopReview

class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = [
            'id', 'product', 'user', 'user_name', 
            'rating', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user']

class ShopReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ShopReview
        fields = [
            'id', 'shop', 'user', 'user_name', 
            'rating', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user']