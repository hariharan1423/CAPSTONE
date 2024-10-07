from django.db import models

# Create your models here.
class CarSale(models.Model):
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    km_driven = models.PositiveIntegerField()
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    fuel = models.CharField(max_length=20)
    seller_type = models.CharField(max_length=20)
    transmission = models.CharField(max_length=20)
    owner = models.CharField(max_length=20)
    mileage = models.FloatField()
    engine = models.FloatField()
    max_power = models.FloatField()
    seats = models.PositiveIntegerField()
    region = models.CharField(max_length=20)

    def __str__(self):
        return self.name