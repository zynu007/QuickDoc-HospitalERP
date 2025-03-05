from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=True)
    address_line1 = forms.CharField(max_length=200, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    pincode = forms.CharField(max_length=10, required=True)
    user_type = forms.ChoiceField(choices=[('patient', 'Patient'), ('doctor', 'Doctor')])
    specialty = forms.ChoiceField(choices=CustomUser.SPECIALTIES, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        user_type = cleaned_data.get('user_type')
        specialty = cleaned_data.get('specialty')

        if password1 and password2 and password1 != password2:
            raise ValidationError("The passwords don't match!")
        
        if user_type == 'doctor' and not specialty:
            raise ValidationError('Please choose your specialty!')

        return cleaned_data
    def save(self, commit = True):
        user = super().save(commit=False)
        
        # Set user type flags
        if self.cleaned_data['user_type'] == 'patient':
            user.is_patient = True
            user.is_doctor = False
            user.specialty = None
        else:
            user.is_doctor = True
            user.is_patient = False
            user.specialty = self.cleaned_data['specialty']

        if commit:
            user.save()
        return user
    

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',
                 'profile_picture', 'address_line1', 'city', 'state', 'pincode', 'user_type',
                 'specialty')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autocomplete': 'username'})
        self.fields['email'].widget.attrs.update({'autocomplete': 'email'})
        self.fields['password1'].widget.attrs.update({'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'autocomplete': 'new-password'})
        self.fields['first_name'].widget.attrs.update({'autocomplete': 'given-name'})
        self.fields['last_name'].widget.attrs.update({'autocomplete': 'family-name'})
        self.fields['address_line1'].widget.attrs.update({'autocomplete': 'address-line1'})
        self.fields['city'].widget.attrs.update({'autocomplete': 'address-level2'})
        self.fields['state'].widget.attrs.update({'autocomplete': 'address-level1'})
        self.fields['pincode'].widget.attrs.update({'autocomplete': 'postal-code'})