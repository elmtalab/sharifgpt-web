from django.urls import path
from .views import RegisterView, LoginView  # Import DashboardView
  # Import the signup view you will create
urlpatterns = [
    path('signupapi/', RegisterView.as_view(), name='signup_api'),
    path('login/', LoginView.as_view(), name='login'),
    
    # ... include other app-specific urls here
]
