from django.db import models
from users.models import CustomUser
from django.utils import timezone



class Appointment(models.Model):
    

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()  # Calculated field (start_time + 45 minutes)
    status = models.CharField(max_length=20, default='CONFIRMED')
    google_calendar_event_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date', '-start_time']
        
    def save(self, *args, **kwargs):
        # Calculate end time (start time + 45 minutes)
        if self.start_time:
            start_datetime = timezone.datetime.combine(
                timezone.datetime.today(), self.start_time
            )
            end_datetime = start_datetime + timezone.timedelta(minutes=45)
            self.end_time = end_datetime.time()
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.patient.first_name} appointment with Dr. {self.doctor.last_name} on {self.appointment_date}"