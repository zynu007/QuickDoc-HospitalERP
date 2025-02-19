from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth import logout

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data.get('user_type')

            if user_type == 'patient':
                user.is_patient = True
            elif user_type == 'doctor':
                user.is_doctor =True

            user.save()
            login(request, user)

            return redirect('login')
    
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', { 'form': form })


@login_required
def dashboard(request):
    if request.user.is_patient:
        return render(request, 'patient_dashboard.html')
    else:
        return render(request, 'doctor_dashboard.html')
    

def custom_logout(request):
    logout(request)
    return redirect('home')  
