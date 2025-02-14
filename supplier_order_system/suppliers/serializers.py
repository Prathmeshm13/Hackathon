from rest_framework import serializers
from .models import Supplier, Product

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "location", "rating"]

class ProductSerializer(serializers.ModelSerializer):
    suppliers = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), many=True, required=False
    )  # Allow multiple suppliers to be assigned

    class Meta:
        model = Product
        fields = ["id", "suppliers", "name", "price", "stock", "delivery_time"]
