from django.contrib import admin

# Register your models here.
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'email', 'created_on')


admin.site.register(User, UserAdmin)


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'parking_spot', 'hours', 'price', 'created_on', 'updated_on')


admin.site.register(Reservation, ReservationAdmin)


class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'name', 'active', 'created_on')

admin.site.register(ParkingSpot, ParkingSpotAdmin)
