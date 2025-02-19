from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)
    address_line1 = forms.CharField(max_length=200, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    pincode = forms.CharField(max_length=10, required=True)
    user_type = forms.ChoiceField(choices=[('patient', 'Patient'), ('doctor', 'Doctor')])


    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',
                 'profile_picture', 'address_line1', 'city', 'state', 'pincode', 'user_type')
        


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add autocomplete attributes
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