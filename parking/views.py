
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from geopy.distance import geodesic
from .models import ParkingSpot, User, Reservation
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

class SignUpView(View):
    def get(self, request):
        return render(request, 'user/signup.html')

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        try:
            user = User.objects.filter(Q(phone_number=phone_number) | Q(email=email)).last()
        except:
            user = ''
        if not user:
            user = User.objects.create(phone_number=phone_number, email=email)
        return redirect('/parking/parking-spots/'+str(user.id)+'/')
        return render(request, 'user/signup.html', {'success': True})

class ParkingSpotsView(View):
    def get(self, request, user):
        parking_spots = ParkingSpot.objects.filter(active=True)
        return render(request, 'parking/parking_spots.html', {'parking_spots': parking_spots, 'user': user})

    def post(self, request, user):
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        radius = float(request.POST.get('radius'))
        parking_spots = ParkingSpot.objects.all()
        nearby_spots = []
        for spot in parking_spots:
            distance = calculate_dist(latitude, longitude, spot.latitude, spot.longitude)
            print(distance, spot.name)
            if distance <= radius:
                nearby_spots.append(spot)
        parking_spots = ParkingSpot.objects.all()
        return render(request, 'parking/parking_spots.html', {'nearby_spots': nearby_spots, 'parking_spots': parking_spots, 'user': user})

class ReservationView(View):
    def get(self, request, user, spot):
        reservations = Reservation.objects.filter(user_id=user)
        price = calculate_price(1)
        return render(request, 'parking/reservation.html', {'user': user, 'price': price, 'spot': spot, 'reservations': reservations})

    def post(self, request, user, spot):
        hours = int(request.POST.get('hours'))
        price = calculate_price(hours)
        reservation = Reservation.objects.create(user_id=user, parking_spot_id=spot, hours=hours, price=price)
        reservations = Reservation.objects.filter(user_id=user)
        return render(request, 'parking/reservation.html', {'price': price, 'user': user, 'spot': spot, 'reservations': reservations})

class UserSignupAPIView(APIView):
    permission_classes = ()

    def post(self, request):
        context = {}
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = request.data['phone_number']
            email = request.data['email']
            try:
                user = User.objects.filter(Q(phone_number=phone_number) | Q(email=email)).last()
            except:
                user = ''
            if not user:
                user = User.objects.create(phone_number=phone_number, email=email)
            context['data'] = UserSerializer(user, many=False).data
            context['msg'] = 'success'
            return Response(context, status=200)
        return Response(serializer.errors, status=201)


class ParkingSpotListAPIView(APIView):
    permission_classes = ()

    def get(self, request):
        parking_spots = ParkingSpot.objects.filter(active=True)
        serializer = ParkingSpotSerializer(parking_spots, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ParkingSpotSearchSerializer(data=request.data)
        if serializer.is_valid():
            latitude = float(request.data['latitude'])
            longitude = float(request.data['longitude'])
            radius = float(request.data['radius'])
            parking_spots = ParkingSpot.objects.all()
            nearby_spots = []
            for spot in parking_spots:
                distance = calculate_dist(latitude, longitude, spot.latitude, spot.longitude)
                if distance <= radius:
                    nearby_spots.append(spot.id)
            parking_spots = ParkingSpot.objects.filter(id__in=nearby_spots, active=True)  # Apply your filter logic here
            serializer = ParkingSpotSerializer(parking_spots, many=True)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class ReservationAPIView(APIView):
    permission_classes = ()

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UserReservationsAPIView(APIView):
    permission_classes = ()

    def get(self, request, user):
        user_reservations = Reservation.objects.filter(user=user)
        serializer = ReservationSerializer(user_reservations, many=True)
        return Response(serializer.data)


def calculate_dist(lat1, lon1, lat2, lon2):
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    # Calculate distance using Vincenty formula
    distance = geodesic(coord1, coord2).meters
    return distance

def calculate_price(hours):
    rate_per_hour = 10  # Set the rate per hour
    price = rate_per_hour * hours
    return price
