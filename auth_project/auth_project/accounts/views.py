# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import get_user_model

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the user immediately after signup
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Custom authentication to allow login with email or username
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            User = get_user_model()
            
            # Try to authenticate the user
            try:
                # First, try to find the user by email
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                # If not found by email, try username
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    # If user not found, show error
                    form.add_error(None, 'Invalid login credentials')
                    return render(request, 'login.html', {'form': form})
            
            # Check password
            if user.check_password(password):
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid login credentials')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'home.html')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')