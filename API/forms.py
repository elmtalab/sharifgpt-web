from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Include the fields you want to show in the form and are present in your CustomUser model
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')  # 'username' should not be here

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        # Include the fields you want to allow to be changed
        fields = ('email', 'first_name', 'last_name')  # 'username' should not be here


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')

    def clean_username(self):
        username = self.cleaned_data['username']
        return username

