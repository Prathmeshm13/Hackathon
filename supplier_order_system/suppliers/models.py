from django.db import models
from users.models import CustomUser

class Supplier(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Product(models.Model):
    suppliers = models.ManyToManyField(Supplier, related_name="products")  # Many-to-Many relationship
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    delivery_time = models.IntegerField(help_text="Estimated delivery time in days")

    def __str__(self):
        return self.name
