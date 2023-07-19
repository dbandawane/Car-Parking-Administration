from django.urls import path
from .views import *



urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('parking-spots/<int:user>/', ParkingSpotsView.as_view(), name='parking_spots'),
    path('reservation/<int:user>/<int:spot>/', ReservationView.as_view(), name='reservation'),


    ### Rest Api's
    path('api/signup/', UserSignupAPIView.as_view(), name='signup_api'),
    path('api/parking-spots/', ParkingSpotListAPIView.as_view(), name='parking_spots_api'),
    path('api/reservation/', ReservationAPIView.as_view(), name='reservation_api'),
    path('api/user-reservations/<int:user>/', UserReservationsAPIView.as_view(), name='user_reservations_api'),
]
