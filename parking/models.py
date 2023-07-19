from django.db import models

# Create your models here.

class User(models.Model):
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    created_on = models.DateTimeField(auto_now_add=True, null=True)


class ParkingSpot(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=50,blank=True, null=True)
    active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    hours = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True)
