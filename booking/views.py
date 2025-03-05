import os
import pickle
import pytz
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment
from users.models import CustomUser
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import AppointmentForm
from django.http import HttpResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from django.conf import settings
from users.models import CustomUser


# Define scopes for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    """
    Retrieve or refresh Google OAuth credentials
    """
    token_path = os.path.join(settings.BASE_DIR, 'token.pkl')
    credentials_path = os.path.join(settings.BASE_DIR, 'credentials.json')
    
    credentials = None
    
    # Try to load existing credentials
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            credentials = pickle.load(token)
    
    # Refresh credentials if expired
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    
    return credentials

def create_google_calendar_event(request, appointment):
    """
    Create a Google Calendar event for an appointment with robust timezone handling
    """
    try:
        # Get credentials
        credentials = get_credentials()
        if not credentials:
            messages.error(request, "Google Calendar authentication failed.")
            return None
        
        # Create service
        service = build('calendar', 'v3', credentials=credentials)
        
        # Set timezone explicitly
        tz = pytz.timezone('Asia/Kolkata')
        
        # Combine date and time with timezone awareness
        start_datetime = tz.localize(datetime.combine(
            appointment.appointment_date, 
            appointment.start_time
        ))
        
        # Calculate end time
        end_datetime = start_datetime + timedelta(minutes=45)
        
        # Create event with timezone-aware datetimes
        event = {
            'summary': f'Appointment with {appointment.patient.first_name}',
            'start': {
                'dateTime': start_datetime.isoformat(),
                'timeZone': str(tz),
            },
            'end': {
                'dateTime': end_datetime.isoformat(),
                'timeZone': str(tz),
            },
            'attendees': [
                {'email': appointment.doctor.email},
            ],
        }
        
        # Insert event
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event.get('id')
    
    except Exception as e:
        messages.error(request, f"Failed to create Google Calendar event: {str(e)}")
        return None

def google_calendar_oauth(request):
    """
    Initiate Google OAuth flow
    """
    credentials_path = os.path.join(settings.BASE_DIR, 'credentials.json')
    
    flow = Flow.from_client_secrets_file(
        credentials_path,
        scopes=SCOPES,
        redirect_uri=request.build_absolute_uri('/oauth2callback/')
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )
    
    request.session['oauth_state'] = state
    return redirect(authorization_url)

def oauth2callback(request):
    """
    Handle OAuth callback and store credentials
    """
    credentials_path = os.path.join(settings.BASE_DIR, 'credentials.json')
    token_path = os.path.join(settings.BASE_DIR, 'token.pkl')
    
    flow = Flow.from_client_secrets_file(
        credentials_path,
        scopes=SCOPES,
        state=request.session.get('oauth_state'),
        redirect_uri=request.build_absolute_uri('/oauth2callback/')
    )
    
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    
    credentials = flow.credentials
    
    # Save credentials
    with open(token_path, 'wb') as token:
        pickle.dump(credentials, token)
        
    request.user.google_calendar_authenticated = True
    request.user.save()
    
    messages.success(request, "Google Calendar successfully authenticated!")
    return redirect('home')



@login_required
def my_bookings(request):
    """View for patients to see their bookings"""
    if request.user.is_patient:
        appointments = Appointment.objects.filter(patient=request.user)
        return render(request, 'booking/my_bookings.html', {'appointments': appointments})
    else:
        messages.error(request, "Only patients can access their bookings.")
        return redirect('dashboard')

@login_required
def doctor_appointments(request):
    """View for doctors to see their appointments"""
    if request.user.is_doctor:
        appointments = Appointment.objects.filter(doctor=request.user)
        return render(request, 'booking/doctor_appointments.html', {'appointments': appointments})
    else:
        messages.error(request, "Only doctors can access their appointments.")
        return redirect('dashboard')

@login_required
def doctor_list(request):
    """View to list all doctors for booking"""
    if request.user.is_patient:
        # Filter doctors who have a specialty
        doctors = CustomUser.objects.filter(is_doctor=True).exclude(specialty__isnull=True)
        return render(request, 'booking/doctor_list.html', {'doctors': doctors})
    else:
        messages.error(request, "Only patients can book appointments.")
        return redirect('dashboard')

def book_appointment(request, doctor_id):
    """View to book an appointment with a specific doctor"""
    if not request.user.is_patient:
        messages.error(request, "Only patients can book appointments.")
        return redirect('dashboard')


def book_appointment(request, doctor_id):
    """View to book an appointment with a specific doctor"""
    if not request.user.is_patient:
        messages.error(request, "Only patients can book appointments.")
        return redirect('dashboard')
    
    doctor = get_object_or_404(CustomUser, id=doctor_id, is_doctor=True)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            appointment.save()  # This will calculate end_time automatically
            
            # Create Google Calendar event only if the appointment is not already confirmed
            event_id = create_google_calendar_event(request, appointment)
            if event_id:
                appointment.google_calendar_event_id = event_id
                appointment.save()
                messages.success(request, "Appointment booked and added to Google Calendar!")
            else:
                messages.warning(request, "Appointment booked, but Google Calendar sync failed.")
    
        return redirect('appointment_confirmation', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    
    return render(request, 'booking/book_appointment.html', {
        'form': form,
        'doctor': doctor
    })




@login_required
def appointment_confirmation(request, appointment_id):
    """View to display appointment confirmation details"""
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    return render(request, 'booking/appointment_confirmation.html', {'appointment': appointment})