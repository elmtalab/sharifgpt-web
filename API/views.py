from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth import login, BACKEND_SESSION_KEY
from django.contrib import messages


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'sharifgpt_website/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            backend = 'django.contrib.auth.backends.ModelBackend'  # Use the appropriate backend that you have configured
            user.backend = backend
            login(request, user, backend=backend)
            return redirect('/dashboard/')  # Use the name of your dashboard url
        return render(request, 'sharifgpt_website/signup.html', {'form': form})


# views.py

from django.shortcuts import render

def signup_view(request):
    # Your signup logic will go here
    return render(request, 'sharifgpt_website/signup.html')  # Make sure the path to signup.html is correct

def dashboard_view(request):
    # Your signup logic will go here
    return render(request, 'sharifgpt_website/dashboard.html')  # Make sure the path to signup.html is correct

from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from .forms import CustomAuthenticationForm  # Make sure to create this form

from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomAuthenticationForm

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = CustomAuthenticationForm()
        return render(request, 'sharifgpt_website/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            backend = 'django.contrib.auth.backends.ModelBackend'
            user = form.get_user()  # Retrieve the user from the form
            login(request, user, backend=backend)  # Now 'user' is defined
            return redirect('dashboard')  # Make sure 'dashboard' is the correct name of your URL pattern
        else:
            messages.error(request, 'نام کاربری یا پسورد اشتباه است')
            return render(request, 'sharifgpt_website/login.html', {'form': form})



from django.shortcuts import render

def home_view(request):
    # Assuming your 'home-6.html' is within a 'sharifgpt_website' subdirectory in your templates
    return render(request, 'sharifgpt_website/home-6.html')




from django.shortcuts import get_object_or_404, render
from .models import Course

def course_detail_view(request, course_id):
    # Get the Course object from the database or return a 404 error if not found
    course = get_object_or_404(Course, pk=course_id)
    
    # Pass the course to the template
    context = {
        'course': course,
        'lessons': course.lessons.all(),
        'reviews': course.reviews.all(),
    }
    return render(request, 'sharifgpt_website/courses-single-3.html', context)