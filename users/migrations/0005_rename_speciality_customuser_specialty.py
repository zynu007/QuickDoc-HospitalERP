# Generated by Django 5.1.6 on 2025-03-05 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_google_calendar_credentials'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='speciality',
            new_name='specialty',
        ),
    ]
