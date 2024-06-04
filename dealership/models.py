# dealership/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# # car model
class Car(models.Model):
    TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('truck', 'Truck'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('hatchback', 'Hatchback'),
        ('minivan', 'Minivan'),
    ]

    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]

    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField()
    image = models.ImageField(upload_to='car_images/')
    image1 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='car_images/', blank=True, null=True)
    car_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='sedan')
    fuel_type = models.CharField(max_length=50, choices=FUEL_CHOICES, default='petrol')
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES, default='manual')
    engine_size = models.DecimalField(max_digits=4, decimal_places=2, default=2.0)  # e.g., 2.0, 3.5
    fuel = models.CharField(max_length=50, default='Gasoline')
    gearbox = models.CharField(max_length=50, default='Automatic')


class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reservation for {self.car} by {self.user} on {self.reservation_date}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    reservations = models.ManyToManyField(Reservation, related_name='reservations', blank=True)

    def __str__(self):
        return self.user.username
