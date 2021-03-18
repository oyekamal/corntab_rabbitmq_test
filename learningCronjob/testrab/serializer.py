from rest_framework import serializers
from .models import Product, Product1

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        


class Product1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product1
        fields = '__all__'
        
