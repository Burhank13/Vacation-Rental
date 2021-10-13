from django.urls import path
from . import views

app_name = "reservations"

urlpatterns = [
    path("create/<int:room>/<int:year>-<int:month>-<int:day>", views.create, name="create"),
    path("<int:pk>/", views.ReservationDetailView.as_view(), name="detail"),
    path("<int:pk>/<str:verb>", views.edit_reservation, name="edit"),
    path("reservationlist", views.reservation_list, name="reservation_list"),
    path("bookings", views.booking_list, name="booking_list"),
]
