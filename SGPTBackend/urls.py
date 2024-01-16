"""SGPTBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from API.views import home_view,signup_view, logout_view,course_listing , ajax_login ,payment_callback, buy_event , user_dashboard,event_detail_view,LoginView,RegisterView ,course_detail_view,checkout,checkout_success #, checkout_success # Import the view you just created
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('API/', include('API.urls')),  # Replace 'appname' with your actual app name
    # ... you can include more app urls if needed
    path('', home_view, name='home'),  # Set the home_view for the root URL
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    
    path('password_reset/', include('django.contrib.auth.urls')),
    path('courses/<str:course_id>/', course_detail_view, name='course_detail'),
    path('checkout/<int:course_id>/', checkout, name='checkout'),
    path('checkout/<int:course_id>/', checkout, name='checkout'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('checkout/success/<int:payment_record_id>/', checkout_success, name='checkout_success'),
    path('event/<slug:slug>/', event_detail_view, name='event_detail'),
    path('event/buy/<slug:slug>/', buy_event, name='buy_event'),

    path('ajax_login/', ajax_login, name='ajax_login'),

    path('payment-callback/', payment_callback, name='payment-callback'),
    path('logout/', logout_view, name='logout'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('courses/', course_listing, name='course_listing'),
    #path('checkout/success/<int:course_id>/', checkout_success, name='checkout_success'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




