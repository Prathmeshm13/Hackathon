from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order
from suppliers.models import Product, Supplier
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        product_name = request.data.get("product_name")
        quantity = request.data.get("quantity")

        # Find the product by name
        products = Product.objects.filter(name__iexact=product_name, stock__gte=quantity)

        if not products.exists():
            return Response({"error": "Product not available in sufficient quantity."}, status=status.HTTP_400_BAD_REQUEST)

        # Select the best supplier based on price, delivery time, and rating
        best_product = (
            products.prefetch_related("suppliers")
            .order_by("price", "delivery_time", "-suppliers__rating")
            .first()
        )

        if not best_product:
            return Response({"error": "No suitable supplier found."}, status=status.HTTP_400_BAD_REQUEST)

        # Select the best supplier for the chosen product
        best_supplier = best_product.suppliers.order_by("-rating").first()

        if not best_supplier:
            return Response({"error": "No supplier found for this product."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order
        order = Order.objects.create(product=best_product, quantity=quantity, supplier=best_supplier)

        # Reduce stock
        best_product.stock -= quantity
        best_product.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
