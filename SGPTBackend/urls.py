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
from API.views import home_view,signup_view , confirm_email ,sharifgpt_name, accounts_page ,ai_account_purchase_success ,payment_callback_ai_account ,checkout_ai_account, buy_ai_account,buy_ai_product , AIProductDetailView,user_events,verify_phone ,AIProductListView, event_list , payment_callback_event ,event_checkout ,event_checkout_success, password_reset , logout_view,course_listing , ajax_login ,payment_callback, buy_event , user_dashboard,event_detail_view,LoginView,RegisterView ,course_detail_view,checkout,checkout_success #, checkout_success # Import the view you just created
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('API/', include('API.urls')),  # Replace 'appname' with your actual app name
    # ... you can include more app urls if needed
    path('', home_view, name='home'),  # Set the home_view for the root URL
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),


    path('sharifgpt-name/', sharifgpt_name, name='sharifgpt_name'),
    
    
    path('password_reset/', include('django.contrib.auth.urls')),
    path('courses/<str:course_id>/', course_detail_view, name='course_detail'),
    path('checkout/<int:course_id>/', checkout, name='checkout'),
    path('checkout/<int:course_id>/', checkout, name='checkout'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('checkout/success/<int:payment_record_id>/', checkout_success, name='checkout_success'),
    path('event/', event_list, name='event_list'),
    path('event/<slug:slug>/', event_detail_view, name='event_detail'),
    path('event/buy/<slug:slug>/', buy_event, name='buy_event'),

    path('ajax_login/', ajax_login, name='ajax_login'),

    path('payment-callback/', payment_callback, name='payment-callback'),
    path('payment-callback-event/', payment_callback_event, name='payment-callback'),
    path('payment-callback-ai-account/', payment_callback_ai_account, name='payment_callback_ai_account'),

    path('logout/', logout_view, name='logout'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('courses/', course_listing, name='course_listing'),
    path('verify_phone/<int:user_id>/', verify_phone, name='verify_phone'),
    path('password_reset/', password_reset, name='password_reset'),

    path('confirm_email/', confirm_email, name='confirm_email'),
    path('verify_phone/<int:user_id>/', verify_phone, name='phone_verification'),
    path('event/checkout/<slug:event_slug>/', event_checkout, name='event_checkout'),
    path('event/checkout_success/<int:payment_record_id>/', event_checkout_success, name='event_checkout_success'),
    
    path('buy-ai-product/<int:ai_product_id>/', buy_ai_product, name='buy_ai_product'),

    path('dshb-events/', user_events, name='user_events'),

    path('shop/', AIProductListView.as_view(), name='shop'),
    path('shop/<slug:slug>/', AIProductDetailView.as_view(), name='product_detail'),
    #path('checkout/success/<int:course_id>/', checkout_success, name='checkout_success'),
    path('buy-ai-account', buy_ai_account, name='buy_ai_account'),
    path('checkout/account-shop/', checkout_ai_account, name='checkout_ai_account'),

    path('ai-account/purchase-success/<int:payment_record_id>/', ai_account_purchase_success, name='ai_account_purchase_success'),

    path('dashboard/accounts/', accounts_page, name='accounts_page'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




