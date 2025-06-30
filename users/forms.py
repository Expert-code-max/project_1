# users/forms.py
from django import forms
from .models import User # Import your custom user model
from django.contrib.auth.hashers import make_password, check_password # For password hashing

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email'] # <-- IMPORTANT: Remove 'password' from fields
                                                                  #     as it will be handled by set_password in save()
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
        }

    # IMPORTANT: Remove the clean_password method entirely!
    # def clean_password(self):
    #    password = self.cleaned_data['password']
    #    # Your logic for not re-hashing on edit is now irrelevant for registration.
    #    # For registration, it should just return the plain password or raise validation errors on strength.
    #    return make_password(password) # THIS WAS THE CULPRIT!

    def clean(self):
        """
        Custom clean method for cross-field validation (e.g., password matching).
        This method runs after individual field clean methods.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2', "Passwords don't match.") # Add error to password2 field

        # You can add other cross-field validations here if needed

        return cleaned_data # Always return cleaned_data from the clean method

    def save(self, commit=True):
        """
        Save method to create the user with a hashed password.
        """
        user = super().save(commit=False) # Get user instance, but don't save to DB yet
        password = self.cleaned_data["password"] # Get the plain-text password from cleaned_data
        user.set_password(password) # Hash and set the password using User model's method (from AbstractBaseUser)

        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This part is for editing existing users, not directly for signup.
        # If the form is used for profile editing where password is optional:
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            self.fields['password2'].required = False # Confirm password also not required on edit

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))