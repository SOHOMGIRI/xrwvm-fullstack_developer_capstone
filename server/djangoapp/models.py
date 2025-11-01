from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# 🔹 Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# 🔹 Car Model model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField(null=True, blank=True)

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('HYPERCAR', 'Hypercar'),
    ]
    type = models.CharField(max_length=15, choices=CAR_TYPES, default='SEDAN')
    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )
    price_usd = models.DecimalField(max_digits=12, decimal_places=2)
    horsepower = models.IntegerField(blank=True, null=True)
    top_speed_kph = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"