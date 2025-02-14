from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Supplier, Product
from .serializers import SupplierSerializer, ProductSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    @action(detail=False, methods=["get"])
    def products(self, request):
        """
        Fetch all products for a given supplier name.
        Expected query param: ?name=<supplier_name>
        """
        supplier_name = request.query_params.get("name")

        if not supplier_name:
            return Response({"error": "Supplier name is required"}, status=400)

        try:
            supplier = Supplier.objects.get(name__iexact=supplier_name)
            products = supplier.products.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

        except Supplier.DoesNotExist:
            return Response({"error": "Supplier not found"}, status=404)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=["get"])
    def suppliers(self, request):
        """
        Fetch all suppliers for a given product name.
        Expected query param: ?name=<product_name>
        """
        product_name = request.query_params.get("name")

        if not product_name:
            return Response({"error": "Product name is required"}, status=400)

        try:
            products = Product.objects.filter(name__iexact=product_name)
            if not products.exists():
                return Response({"error": "Product not found"}, status=404)

            suppliers = set()
            for product in products:
                suppliers.update(product.suppliers.all())  # Get all related suppliers

            serializer = SupplierSerializer(suppliers, many=True)
            return Response(serializer.data)

        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
