# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout # Import auth functions
from django.contrib.auth.decorators import login_required # Decorator for protected views
from django.contrib.auth.hashers import make_password, check_password # For manual password hashing/checking if not using AUTH_USER_MODEL directly
from .models import User
from .forms import UserRegisterForm, UserLoginForm

# Add set_password method to UserProfile model dynamically if not inherited from AbstractUser
# This is a workaround if UserProfile does not inherit from AbstractUser and you want to use set_password/check_password syntax
def set_password_for_userprofile(self, raw_password):
    self.password = make_password(raw_password)

def check_password_for_userprofile(self, raw_password):
    return check_password(raw_password, self.password)

User.add_to_class('set_password', set_password_for_userprofile)
User.add_to_class('check_password', check_password_for_userprofile)


def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save the user with hashed password handled by form's save method
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login') # Redirect to login page after successful registration
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user using the custom UserProfile model
            # Django's authenticate will work if AUTH_USER_MODEL is set
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user) # Log the user in to create a session
                messages.success(request, f'Welcome, {username}!')
                return redirect('user_profile') # Redirect to user profile after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required # Ensures only logged-in users can access this view
def user_profile(request):
    # request.user will now be an instance of your UserProfile model
    # thanks to AUTH_USER_MODEL setting and login function.
    user = request.user
    return render(request, 'user_profile.html', {'user': user})

def logout_user(request):
    logout(request) # Log the user out to destroy their session
    messages.info(request, 'You have been logged out.')
    return redirect('product_list') # Redirect to product list or home page