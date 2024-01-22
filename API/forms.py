

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'password1', 'password2', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user




# Inside your API/forms.py

from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user



from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')

    def clean_username(self):
        username = self.cleaned_data['username']
        return username

