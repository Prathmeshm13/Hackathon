from rest_framework import serializers
from .models import Order
from suppliers.models import Product, Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "location", "rating"]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock", "delivery_time"]

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    supplier = SupplierSerializer()

    class Meta:
        model = Order
        fields = "__all__"
