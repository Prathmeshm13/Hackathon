from django.urls import path, include
from rest_framework.routers import DefaultRouter
from suppliers.views import SupplierViewSet, ProductViewSet
from orders.views import OrderViewSet
from django.contrib import admin

router = DefaultRouter()
router.register(r"suppliers", SupplierViewSet)
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/", include(router.urls)),
]
