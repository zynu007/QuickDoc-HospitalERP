from django.urls import path
from . import views

urlpatterns =[
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('doctor-appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('confirmation/<int:appointment_id>/', views.appointment_confirmation, name='appointment_confirmation'),
    path('google-calendar-auth/', views.google_calendar_oauth, name='google_calendar_auth'),
]