from decimal import Decimal
from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=500)


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, source='name')
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    unit_price_after_tax = serializers.SerializerMethodField()
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name='category-detail',
    )
        
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'inventory', 'category', 'unit_price_after_tax']
    
    def get_unit_price_after_tax(self, product):
        return round(product.unit_price * Decimal(1.09), 2)
