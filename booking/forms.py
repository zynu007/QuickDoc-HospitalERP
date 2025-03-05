from django import forms
from django.core.exceptions import ValidationError
from .models import Appointment
from datetime import datetime, time, timedelta

class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select a date for your appointment"
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        help_text="Select a start time (9:00 AM - 8:00 PM)"
    )
    
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'start_time']
    
    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        start_time = cleaned_data.get('start_time')
        
        # Check if date is in the past
        if appointment_date and appointment_date < datetime.now().date():
            raise ValidationError("Cannot book an appointment in the past.")
        
        # Check if time is within business hours (9 AM - 8 PM)
        if start_time:
            business_start = time(9, 0)  # 9:00 AM
            business_end = time(20, 0)   # 8:00 PM
            
            if start_time < business_start or start_time > business_end:
                raise ValidationError("Appointments are only available between 9:00 AM and 8:00 PM.")
        
        return cleaned_data