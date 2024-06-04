# dealership/admin.py

from django.contrib import admin
from .models import Car, Profile, Reservation

#Register the Car model in the admin interface to allow easy data entry.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'price', 'mileage', 'car_type', 'fuel_type', 'transmission', 'engine_size')#fields to display as columns in the list view of the admin interface.
    list_filter = ('make', 'model', 'fuel', 'gearbox', 'year', 'price') #adds filter controls to the right sidebar of the change list page
    search_fields = ('make', 'model', 'year') #Adds a admin search box for records based on the specified fields

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'reservation_date')