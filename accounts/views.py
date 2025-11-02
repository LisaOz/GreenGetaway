from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView

# Create your views here.

"""
View for registration form. When the user is registered, he is redirected to the login page
"""

# ---------------------------

# Registration View

# ---------------------------

def register(request):
    """
    Handles user registration.
    GET: Show an empty registration form.
    POST: Validate and create a new user.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created successfully for {user.username}! You can now log in.")
            return redirect('accounts:login')
    else:
        # This part was previously missing or mis-indented
        form = UserCreationForm()

    # Always return the template with the form (even if invalid)
    return render(request, 'accounts/register.html', {'form': form})

# ---------------------------

# Login View

# ---------------------------

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages



def login(request):
    """
    Handles user login for GET and POST requests.
    GET: displays empty login form
    POST: validates form and logs in user
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Get user from the form
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('getaway:home')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# ---------------------------

# Dashboard View

# ---------------------------

@login_required
def dashboard(request):
    """
    Shows a user's dashboard.
    ow it  displays a placeholder list of trips; will be replaced it with your booking model.
    """
    user = request.user
    # trips = user.bookedtrip_set.all()  # Uncomment when you have a booking model
    trips = []  # placeholder
    return render(request, 'accounts/dashboard.html', {'trips': trips})

# ---------------------------

# Logout View

# ---------------------------

@login_required
def logout(request):
    """
    Logs out the current user and redirects to the login page.
    """
    auth_logout(request)
    return redirect('accounts:login')

# ---------------------------

# Password Reset Views

# ---------------------------

class CustomPasswordResetView(PasswordResetView):
    """
    Initiates password reset via email.
    """
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    Displays a confirmation that password reset email was sent.
    """
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Allows the user to set a new password after clicking the reset link.
    """
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:login')


"""

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'getaway/accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    trips = user.bookedtrip_set.all()  # TODO: add a booking model
    return render(request, 'accounts/dashboard.html', {'trips': trips})


"""
