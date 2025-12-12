from django import forms
from django.core.exceptions import ValidationError
import re

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'form-input'
        })
    )
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-input'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput()
    )

    # Validate username format
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4 or len(username) > 20:
            raise ValidationError("Username must be between 4 and 20 characters.")
        if not re.match(r'^[A-Za-z][A-Za-z0-9_]*$', username):
            raise ValidationError(
                "Username must start with a letter and contain only letters, numbers, or underscores."
            )
        return username

    # Optional: you can also validate password format if you want
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password
