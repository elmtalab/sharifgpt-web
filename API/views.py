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

from .utils import make_payment, process_payment_response


from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth import login

import random
import datetime
from django.shortcuts import redirect, render
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .models import CustomUser





class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'sharifgpt_website/signup.html', {'form': form})
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Generate a verification code
            user.verification_code = str(random.randint(100000, 999999))
            user.code_expires = timezone.now() + datetime.timedelta(minutes=5)
            user.save()

            # Send verification SMS
            send_verification_message(user.phone_number, user.verification_code)

            # Redirect to verification page
            return redirect('verify_phone', user_id=user.id)
        return render(request, 'sharifgpt_website/signup.html', {'form': form})


# views.py

from django.shortcuts import render

def signup_view(request):
    # Your signup logic will go here
    return render(request, 'sharifgpt_website/signup.html')  # Make sure the path to signup.html is correct



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
            return redirect('user_dashboard')  # Make sure 'dashboard' is the correct name of your URL pattern
        else:
            messages.error(request, 'نام کاربری یا پسورد اشتباه است')
            return render(request, 'sharifgpt_website/login.html', {'form': form})



from django.shortcuts import render

def home_view(request):
    # Assuming your 'home-6.html' is within a 'sharifgpt_website' subdirectory in your templates
    return render(request, 'Landing/demo-3.html')




from django.shortcuts import get_object_or_404, render
from .models import Course,Enrollment

def course_detail_view(request, course_id):
    # Get the Course object from the database or return a 404 error if not found
    course = get_object_or_404(Course, pk=course_id)
    instructor = course.instructor

    # Pass the course and instructor to the template
    context = {
        'course': course,
        'instructor': instructor,  # Add this line
        'lessons': course.lessons.all(),
        'reviews': course.reviews.all(),
    }
    # Pass the course to the template
    return render(request, 'sharifgpt_website/courses-single-3.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.utils import timezone
from .models import Course, PaymentRecord, PaymentStatus
# Assuming make_payment is defined elsewhere in your project

def checkout(request, course_id=None):
    if request.method == 'GET':
        if course_id is not None:
            course = get_object_or_404(Course, pk=course_id)
            final_price = course.discounted_price if course.discounted_price else course.original_price
            context = {
                'course': course,
                'final_price': final_price,
            }
            return render(request, 'sharifgpt_website/shop-checkout.html', context)
        else:
            return redirect('home')

    elif request.method == 'POST':
        # Initialize payment_record outside the try block to access it in the except block
        payment_record = None

        try:
            # Extract form data
            firstName = request.POST.get('firstName', '').strip()
            lastName = request.POST.get('lastName', '').strip()
            phone = request.POST.get('phone', '').strip()
            email = request.POST.get('email', '').strip()
            payment_method = request.POST.get('payment_method', '').strip()
            course_id = request.POST.get('course_id', '').strip()

            # Validate form data
            if not all([firstName, lastName, phone, email, payment_method, course_id]):
                raise ValueError('All required fields must be filled.')
            validate_email(email)

            # Retrieve the course object
            course = get_object_or_404(Course, pk=course_id)
            # Check if user exists or create new user




            user, created = CustomUser.objects.get_or_create(email=email, defaults={
                'phone_number': phone,
                'first_name': firstName,
                'last_name': lastName
            })

            if created:
                # If user is created, set a random password (or your own logic)
                user.set_password(str(random.randint(100000, 99999999)))
                user.save()
            
            # Authenticate and login the user
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')








            # Create a payment record
            payment_record = PaymentRecord.objects.create(
                user=user,
                course=course,
                status=PaymentStatus.INITIATED,
                payment_method=payment_method,
                amount_paid=course.discounted_price if course.discounted_price else course.original_price,
                created_at=timezone.now()
            )

            # Initiate the payment process
            amount_paid_str = int(payment_record.amount_paid)
            payment_response = make_payment("65a14466c5d2cb001d8d45ce", amount_paid_str, "http://sharifgpt.com/payment-callback/")
            print(payment_response)
            payment_response = process_payment_response(payment_response)
            if not payment_response.get("status") == "success":
                raise ValueError(payment_response.get("message", "Payment failed with no error message."))

            # Process the payment response
            if payment_response.get("status") == "success":
                payment_record.track_id = payment_response.get("trackId")
                payment_record.payment_message = payment_response.get("message")
                payment_record.status = PaymentStatus.SUCCESS
            else:
                payment_record.status = PaymentStatus.FAILED
                payment_record.error_message = payment_response.get("error", "Unknown error")

            payment_record.save()

            # Redirect based on payment status
            if payment_response.get("status") == "success":
                print("here")
                payment_record.track_id = payment_response.get("trackId")
                payment_record.payment_message = payment_response.get("message")
                payment_record.status = PaymentStatus.SUCCESS
                payment_record.save()

                # Redirect the user to the Zibal payment page
                zibal_payment_url = f"https://gateway.zibal.ir/start/{payment_record.track_id}"
                return redirect(zibal_payment_url)

            else:
                payment_record.status = PaymentStatus.FAILED
                payment_record.error_message = payment_response.get("error", "Unknown error")
                payment_record.save()
                messages.error(request, 'An error occurred during checkout.')
                return redirect('checkout', course_id=course_id)

        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            if payment_record:
                payment_record.status = PaymentStatus.FAILED
                payment_record.error_message = str(e)
                payment_record.save()
        except ValueError as e:
            if payment_record:
                payment_record.status = PaymentStatus.FAILED
                payment_record.error_message = str(e)
                payment_record.save()
            messages.error(request, str(e))
        except Exception as e:
            if payment_record:
                payment_record.status = PaymentStatus.FAILED
                payment_record.error_message = str(e)
                payment_record.save()
            messages.error(request, 'An error occurred during checkout.')
        return redirect('checkout', course_id=course_id)

    else:
        return redirect('home')


from django.shortcuts import render, get_object_or_404
from .models import Course, PaymentRecord

def checkout_success(request, payment_record_id):
    # Retrieve the payment record and the associated course
    payment_record = get_object_or_404(PaymentRecord, id=payment_record_id)
    course = get_object_or_404(Course, pk=payment_record.course.pk)

    # Format the date and price
    order_number = payment_record.id
    order_date = payment_record.created_at.strftime('%Y/%m/%d')
    final_price = "{:,.2f}".format(payment_record.course.discounted_price if payment_record.course.discounted_price else payment_record.course.original_price)
    payment_method = 'درگاه بانک سامان'  # Replace with dynamic data if needed

    # Prepare the context
    context = {
        'course': course,
        'order_number': order_number,
        'order_date': order_date,
        'final_price': final_price,
        'payment_method': payment_method,
        'message': 'Thank you for your purchase!',
    }

    # Render the template
    return render(request, 'sharifgpt_website/shop-order.html', context)






import requests

def send_verification_message(receptor, param1, apikey="0241b2afd033139722a2c8baafe771917ca70ed35709d82054deb6c347b65f04", template="sharifgpt"):
    """
    Send a verification message using Ghasedak API.

    Args:
    receptor (str): The phone number to which the message is sent.
    param1 (str): The parameter value to be sent in the message.
    apikey (str): The API key for Ghasedak API. Default is set to a provided key.
    template (str): The template name for the message. Default is 'test'.

    Returns:
    str: The response text from the API call.
    """

    url = "https://api.ghasedak.me/v2/verification/send/simple"
    payload = f"receptor={receptor}&template={template}&type=1&param1={param1}"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'apikey': apikey,
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text

# Example usage
# response = send_verification_message("09109008317", "test1")
# print(response)







from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Enrollment

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Enrollment, CustomUser
from django.urls import reverse

@login_required
def user_dashboard(request):
    user = request.user
    if not user.is_phone_verified:
        # Redirect to password reset page
        return redirect('password_reset')

    enrollments = Enrollment.objects.filter(user=user)
    courses = [enrollment.course for enrollment in enrollments]
    context = {'courses': courses}
    return render(request, 'sharifgpt_website/dshb-bookmarks.html', context)





from django.shortcuts import render, get_object_or_404
from .models import Event

def event_detail_view(request, slug):
    event = get_object_or_404(Event, slug=slug)
    speakers = event.speakers.all()  # Fetch speakers for the event
    return render(request, 'sharifgpt_website/event-single.html', {'event': event, 'speakers': speakers})



def sharifgpt_name(request):
    
    return render(request, 'sharifgpt_website/sharifgpt-name.html')





from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def buy_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    
    if request.method == 'POST':
        # You would get the quantity from the form. Here it's hardcoded to 1 for simplicity.
        quantity = 1
        total_price = event.price * quantity * (1 - (event.discount / 100))
        
        Booking.objects.create(
            user=request.user,
            event=event,
            quantity=quantity,
            total_price=total_price
        )
        messages.success(request, 'Thank you for purchasing the event!')
        return redirect('event_detail', slug=slug)

    return render(request, 'sharifgpt_website/checkout-events.html', {'event': event})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event, EventPaymentRecord
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Note: The IPG integration and `make_payment` function should be defined according to your payment gateway's API.

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event, EventPaymentRecord, CustomUser
import random

from django.db.models import Q

# Your make_payment and process_payment_response functions should be defined elsewhere


def event_checkout(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    final_price = event.price * (1 - event.discount / 100)

    if request.method == 'GET':
        context = {
            'event': event,
            'final_price': final_price,
        }
        return render(request, 'sharifgpt_website/checkout-events.html', context)

    elif request.method == 'POST':
        payment_record = None
        try:
            # Extract form data
            firstName = request.POST.get('firstName', '').strip()
            lastName = request.POST.get('lastName', '').strip()
            phone = request.POST.get('phone', '').strip()
            email = request.POST.get('email', '').strip()
            payment_method = request.POST.get('payment_method', '').strip()

            print("Form Data:", firstName, lastName, phone, email, payment_method)

            # Validate form data
            if not all([firstName, lastName, phone, email]):
                print("dfkbgjfhjfgb")
                raise ValueError('All required fields must be filled.')

            # Check if user exists or create new user
            user = CustomUser.objects.filter(Q(email=email) | Q(phone_number=phone)).first()
            if user:
                # User exists, check if the names and email match
                if user.first_name != firstName or user.last_name != lastName or user.email != email:
                    # For security, don't give specifics - just say a match couldn't be found
                    # TODO user give different information than what he really have
                    # it should throw out errors
                    pass
            else:
                # Create new user
                user = CustomUser.objects.create_user(
                    email=email,
                    phone_number=phone,
                    first_name=firstName,
                    last_name=lastName
                )
                # Set a random password (or your own logic)
                user.set_password(str(random.randint(100000, 99999999)))
                user.save()

            # Authenticate and login the user
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Create a payment record

           
            # Initiate the payment process
            amount_paid = int(final_price)
            print("here1")
            payment_response = make_payment("65a14466c5d2cb001d8d45ce", amount_paid, "http://sharifgpt.com/payment-callback-event/")

            print("here2")
            payment_response = process_payment_response(payment_response)


            payment_record = EventPaymentRecord.objects.create(
                user=request.user,
                event=event,
                status='INITIATED',
                payment_method=payment_method,
                amount_paid=amount_paid,
                created_at=timezone.now(),
                track_id=payment_response.get("trackId")
            )
                        
            print("Payment Response:", payment_response)
            print("Type:", type(payment_response))

            if payment_response.get("status") != "success":
                raise ValueError(payment_response.get("message", "Payment failed with no error message."))

            # Redirect based on payment status
            if payment_response.get("status") == "success":
                payment_record.track_id = payment_response.get("trackId")
                payment_record.payment_message = payment_response.get("message")
                payment_record.status = 'SUCCESS'
                payment_record.save()

                # Redirect the user to the payment page (e.g., Zibal payment page)
                payment_page_url = f"https://gateway.zibal.ir/start/{payment_record.track_id}"
                return redirect(payment_page_url)
            else:
                raise ValueError(payment_response.get("error", "Unknown error"))

        except ValidationError as e:
            messages.error(request, f'Validation error: {e.message}')
        except ValueError as e:
            messages.error(request, f'Value error: {str(e)}')
        except Exception as e:
            # It's often useful to log the full exception details in your server logs,
            # especially for unexpected exceptions, to aid in debugging.
            
            messages.error(request, f'An unexpected error occurred: {str(e)}')

            if payment_record:
                payment_record.status = 'FAILED'
                payment_record.error_message = str(e) if isinstance(e, Exception) else 'An unknown error occurred'
                payment_record.save()

        return redirect('event_checkout', event_slug=event_slug)

    return redirect('home')


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import EventPaymentRecord, Event
from django.contrib import messages

@login_required
def event_checkout_success(request, payment_record_id):
    # Retrieve the payment record and the associated event
    payment_record = get_object_or_404(EventPaymentRecord, id=payment_record_id, user=request.user)
    event = get_object_or_404(Event, id=payment_record.event.id)

    # Check the payment status
    if payment_record.status != 'SUCCESS':
        messages.error(request, "There was a problem with your payment. Please contact support.")
        return redirect('event_detail', slug=event.slug)

    # Format the date and price
    order_number = payment_record.id
    order_date = payment_record.created_at.strftime('%Y/%m/%d')
    final_price = "{:,.2f}".format(payment_record.amount_paid)
    payment_method = payment_record.payment_method  # Adjust according to your payment method field

    # Prepare the context
    context = {
        'event': event,
        'order_number': order_number,
        'order_date': order_date,
        'final_price': final_price,
        'payment_method': payment_method,
        'message': 'Thank you for reserving the event!',
    }

    # Render the template
    return render(request, 'sharifgpt_website/event-order-success.html', context)









from django.http import JsonResponse
from django.contrib.auth import authenticate, login

def ajax_login(request):
    if request.method == 'POST' and request.is_ajax():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})

    return render(request, 'your_template.html')




from django.urls import reverse


from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment, PaymentRecord
import requests
from .models import Enrollment  # Adjust the import path based on your project structure


from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import PaymentRecord, Event, Enrollment, Booking, Course
import requests
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()




from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment, PaymentRecord
import requests

@csrf_exempt
def payment_callback(request):
    if request.method == 'GET':
        # Extract callback data
        track_id = request.GET.get('trackId')
        success = request.GET.get('success') == '1'
        status = int(request.GET.get('status'))
        order_id = request.GET.get('orderId', '')

        # Verify the payment
        verify_url = "https://gateway.zibal.ir/v1/verify"
        verify_data = {
            "merchant": "65a14466c5d2cb001d8d45ce",  # Replace with your actual merchant ID
            "trackId": track_id,
        }
        response = requests.post(verify_url, json=verify_data)

        if response.ok:
            verify_result = response.json()
            # Save payment information
            payment = Payment.objects.create(
                track_id=track_id,
                order_id=order_id,
                success=success,
                status=status,
                paid_at=verify_result.get('paidAt'),
                card_number=verify_result.get('cardNumber'),
                amount=verify_result.get('amount'),
                ref_number=verify_result.get('refNumber'),
                description=verify_result.get('description'),
                result_code=verify_result.get('result'),
                message=verify_result.get('message')
            )

            # TODO: Replace the placeholders below with actual logic to determine the user and course
            user = request.user  # This assumes your user is logged in and available in request.user
            payment_record = PaymentRecord.objects.get(track_id=track_id)
            corresponding_course = payment_record.course

            # Create a PaymentRecord instance
            payment_record = PaymentRecord.objects.create(
                user=user,
                course=corresponding_course,
                status='success',  # or use PaymentStatus.SUCCESS if you have a choice field
                transaction_id=track_id,
                payment_method="Your payment method",  # Set the payment method, adjust as needed
                amount_paid=verify_result.get('amount'),
                # ... set other required fields ...
            )

            # Redirect to the checkout success page
            return HttpResponseRedirect(reverse('checkout_success', args=[payment_record.id]))
        else:
            return JsonResponse({"error": "Failed to verify payment"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)








@csrf_exempt
def payment_callback_event(request):
    user = request.user
    if request.method == 'GET':
        track_id = request.GET.get('trackId')
        success = request.GET.get('success') == '1'
        status = int(request.GET.get('status'))
        
        # Verify the payment
        verify_url = "https://gateway.zibal.ir/v1/verify"
        verify_data = {
            "merchant": "65a14466c5d2cb001d8d45ce",  # Replace with your actual merchant ID
            "trackId": track_id,
        }
        response = requests.post(verify_url, json=verify_data)
        
        if response.ok:
            verify_result = response.json()
            print(verify_result)
            payment_record = EventPaymentRecord.objects.filter(track_id=track_id).first()
            if payment_record is None:
                return JsonResponse({"error": "Payment record not found"}, status=404)

            if success:
                # Extract amount from verify_result, ensuring it's available and valid
                amount_paid = verify_result.get('amount')
                if amount_paid is None:
                    return JsonResponse({"error": "Amount paid data not found in payment verification"}, status=400)

                payment_record.status = 'SUCCESS'
                payment_record.transaction_id = verify_result.get('refNumber')
                payment_record.payment_method = "Zibal"  # Adjust as needed
                payment_record.amount_paid = amount_paid
                payment_record.payment_message = verify_result.get('message')
                payment_record.payment_details = verify_result
                payment_record.save()

                
                # Logic for event payment, such as creating a booking
                if not Booking.objects.filter(user=user, event=payment_record.event).exists():
                    Booking.objects.create(
                        user=user,
                        event=payment_record.event,
                        quantity=1,  # Update with actual quantity if needed
                        total_price=payment_record.amount_paid
                    )
            else:
                payment_record.status = 'FAILED'
                payment_record.error_message = verify_result.get('message')
                payment_record.save()
                return JsonResponse({"error": "Payment verification failed"}, status=400)

            # Redirect to the appropriate success page
            
            
            return HttpResponseRedirect(reverse('event_checkout_success', args=[payment_record.id]))
        else:
            return JsonResponse({"error": "Failed to verify payment"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)




from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to homepage or any other page





from django.shortcuts import render
from .models import Course

def course_listing(request):
    courses = Course.objects.all()  # Get all courses
    return render(request, 'sharifgpt_website/courses-list-7.html', {'courses': courses})





from .models import CustomUser

def verify_phone(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        
    except CustomUser.DoesNotExist:
        # Handle user not found
        
        pass

    if request.method == 'POST':
        code = request.POST.get('code')
        if user.verification_code == code and user.code_expires > timezone.now():
            user.is_phone_verified = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/dashboard/')
        else:
            # Handle invalid or expired code
            pass
    
    return render(request, 'sharifgpt_website/verify_phone.html', {'user_id': user_id})






from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect

@login_required
def password_reset(request):
    user = request.user
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Keep the user logged in after password change
        if not user.is_phone_verified:
            user.verification_code = str(random.randint(100000, 999999))
            user.code_expires = timezone.now() + datetime.timedelta(minutes=5)
            user.save()

            # Send verification SMS
            send_verification_message(user.phone_number, user.verification_code)
            # Redirect to phone verification page
            return redirect('phone_verification', user_id=user.id)
        else:
            # If phone is already verified, go to the dashboard
            return redirect('user_dashboard')
        return redirect('phone_verification', user_id=request.user.id)

    return render(request, 'sharifgpt_website/password_reset.html')






# views.py

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Event,EventCategory

def event_list(request):
    event_list_all = Event.objects.all()  # Retrieves all events; adjust query as needed
    page = request.GET.get('page', 1)
    categories = EventCategory.objects.all()
    paginator = Paginator(event_list_all, 6)  # Show 6 events per page
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    context = {
        'events': events,
        'current_page': page,
        'total_pages': paginator.num_pages,
        'categories': categories
    }

    return render(request, 'sharifgpt_website/event-list-1.html', context)





from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Booking
from django.contrib.auth.decorators import login_required

@login_required
def user_events(request):
    # Get all bookings for the current user with related event data
    bookings = Booking.objects.filter(user=request.user).select_related('event')
    
    # Extract the event instances from the bookings
    events_list = [booking.event for booking in bookings]
    
    # Set up pagination
    paginator = Paginator(events_list, 6)  # Show 6 events per page
    page = request.GET.get('page', 1)  # Get the page number from the request

    try:
        purchased_events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        purchased_events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        purchased_events = paginator.page(paginator.num_pages)

    return render(request, 'sharifgpt_website/dshb-events.html', {
        'purchased_events': purchased_events
    })













from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import AIProduct, AIProductReview

class AIProductListView(View):
    def get(self, request):
        products = AIProduct.objects.all()
        paginator = Paginator(products, 10)  # Show 10 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'sharifgpt_website/shop-list.html', {'page_obj': page_obj})

from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import AIProduct

class AIProductDetailView(View):
    def get(self, request, slug):
        # Fetch the product by slug. If it doesn't exist, it will raise a 404 error.
        product = get_object_or_404(AIProduct, slug=slug)

        # The context dictionary will be passed to the template. It contains the product instance.
        # The template will be able to access the product's details, including any related images
        # if the images are accessible via a related name (e.g., product.images.all).
        context = {
            'product': product
        }

        # The template 'sharifgpt_website/shop-single.html' will be rendered using the context.
        # Replace 'sharifgpt_website/shop-single.html' with the path to your actual template if different.
        return render(request, 'sharifgpt_website/shop-single.html', context)


class AIProductReviewView(View):
    def post(self, request, product_id):
        # Assume form data is sent via POST request
        product = get_object_or_404(AIProduct, pk=product_id)
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')
        user = request.user  # Assumes user authentication
        AIProductReview.objects.create(product=product, user=user, review_text=review_text, rating=rating)
        return redirect('ai_product_detail', slug=product.slug)







# path/filename: views.py

from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import AIProduct, PaymentRecord  # Assuming you have these models
 # Assuming you have a function for initiating payment

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import AIProduct, PaymentRecord


@login_required
def buy_ai_product(request, ai_product_id):
    """
    View to handle AI product purchase and initiate the payment process.
    """
    ai_product = get_object_or_404(AIProduct, id=ai_product_id)
    price = ai_product.price  # Assuming price is the total price to pay
    payment_record = None
    try:
        
        # Initiate the payment process
        payment_response = make_payment("65a14466c5d2cb001d8d45ce", int(price), "http://sharifgpt.com/payment-callback-ai-account/")
        print(payment_response)
        payment_response = process_payment_response(payment_response)

        # Create a payment record
        payment_record = PaymentRecord.objects.create(
            user=request.user,
            product=ai_product,
            status='INITIATED',
            payment_method='YourPaymentMethod',  # Replace with actual payment method
            amount_paid=price,
            created_at=timezone.now(),
            track_id=payment_response.get("trackId")
        )

        if payment_response.get("status") != "success":
            raise ValueError(payment_response.get("message", "Payment failed with no error message."))

        # Redirect based on payment status
        if payment_response.get("status") == "success":
            payment_record.status = 'SUCCESS'
            payment_record.payment_message = payment_response.get("message")
            payment_record.save()

            # Redirect the user to the payment page (e.g., Zibal payment page)
            payment_page_url = f"https://gateway.zibal.ir/start/{payment_record.track_id}"
            return redirect(payment_page_url)
        else:
            raise ValueError(payment_response.get("error", "Unknown error"))

    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {str(e)}')
        payment_record.status = 'FAILED'
        payment_record.error_message = str(e)
        payment_record.save()
        return redirect('ai_product_detail', id=ai_product_id)




from django.http import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

@require_POST
def buy_ai_account(request):
    ai_account_id = request.POST.get('ai_account_id')
    
    if request.user.is_authenticated:
        # If user is logged in, redirect to 'buy_ai_product'
        return HttpResponseRedirect(reverse('buy_ai_product', args=[ai_account_id]))
    else:
        # If user is not logged in, save the ai_account_id in the session
        request.session['ai_account_id_for_purchase'] = ai_account_id
        # And redirect to login with the 'next' parameter set to the checkout page
        checkout_url = reverse('checkout_ai_account') 
        
        return redirect(checkout_url)







from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.contrib.auth import login
import random
from .models import AIProduct, CustomUser

AIAccountPaymentRecord=PaymentRecord
@require_http_methods(["GET", "POST"])
def checkout_ai_account(request):
    ai_account_id = request.session.get('ai_account_id_for_purchase')
    ai_account = get_object_or_404(AIProduct, id=ai_account_id)
    final_price = ai_account.price  # Assuming there's no discount for AI account

    if request.method == 'GET':
        context = {
            'ai_account': ai_account,
            'final_price': final_price,
        }
        return render(request, 'sharifgpt_website/account-shop-checkout.html', context)

    elif request.method == 'POST':
        payment_record = None
        with transaction.atomic():
            try:
                # Extract form data
                firstName = request.POST.get('firstName', '').strip()
                lastName = request.POST.get('lastName', '').strip()
                phone = request.POST.get('phone', '').strip()
                email = request.POST.get('email', '').strip()
                payment_method = request.POST.get('payment_method', '').strip()

                # Validate form data
                if not all([firstName, lastName, phone, email]):
                    raise ValidationError('All required fields must be filled out.')

                # Check if user exists
                user = User.objects.filter(Q(email=email) | Q(phone_number=phone)).first()
                if not user:
                    # Create new user if it does not exist
                    user = User.objects.create_user(
                        email=email,
                        phone_number=phone,
                        first_name=firstName,
                        last_name=lastName
                    )
                    # Set a random password (or your own logic)
                    user.set_password(User.objects.make_random_password())
                    user.save()
                else:
                    # Here you can handle if the user exists but the names do not match.
                    # For now, we'll assume they match and proceed.
                    # You may want to log in the user or handle it differently.
                    pass

                # Authenticate and login the user
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                
                # Initiate the payment process and create a payment record
                amount_paid = int(final_price)
                payment_response = make_payment("65a14466c5d2cb001d8d45ce", int(amount_paid), "http://sharifgpt.com/payment-callback-ai-account/")
                payment_response = process_payment_response(payment_response)
                payment_record = AIAccountPaymentRecord.objects.create(
                    user=user,
                    product=ai_account,
                    status='INITIATED',
                    payment_method=payment_method,
                    amount_paid=amount_paid,
                    created_at=timezone.now(),
                    track_id=payment_response.get("trackId")
                )

                if payment_response.get("status") != "success":
                    raise ValueError(payment_response.get("message", "Payment failed with no error message."))

                # Handle successful payment response
                if payment_response.get("status") == "success":
                    payment_record.status = 'SUCCESS'
                    payment_record.payment_message = payment_response.get("message")
                    payment_record.save()

                    # Redirect to payment page
                    payment_page_url = f"https://gateway.zibal.ir/start/{payment_record.track_id}"
                    return redirect(payment_page_url)

            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {str(e)}')
                if payment_record:
                    payment_record.status = 'FAILED'
                    payment_record.error_message = str(e)
                    payment_record.save()

        # In case of error, redirect back to the checkout page
        return redirect('checkout_ai_account')  # Adjust this URL name to your actual checkout URL name for AI accounts

    # Redirect to home as a fallback
    return redirect('home')













from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import PaymentRecord, AIProduct, Booking ,UserAIAccount   # Make sure to import the correct models

@csrf_exempt
def payment_callback_ai_account(request):
    if request.method == 'GET':
        track_id = request.GET.get('trackId')
        success = request.GET.get('success') == '1'
        
        # Verify the payment
        verify_url = "https://gateway.zibal.ir/v1/verify"
        verify_data = {
            "merchant": "65a14466c5d2cb001d8d45ce",  # Replace with your actual merchant ID
            "trackId": track_id,
        }
        response = requests.post(verify_url, json=verify_data)
        
        if response.ok:
            verify_result = response.json()
            # Assuming 'PaymentRecord' is used for AI account payments as well
            payment_record = PaymentRecord.objects.filter(track_id=track_id, product__isnull=False).first()
            if payment_record is None:
                return JsonResponse({"error": "Payment record not found"}, status=404)

            if success:
                # Update the payment record with the success status and other details
                payment_record.status = 'SUCCESS'
                payment_record.transaction_id = verify_result.get('refNumber')
                payment_record.payment_method = "Zibal"
                payment_record.amount_paid = verify_result.get('amount')  # Default to 0 if not found
                payment_record.payment_message = verify_result.get('message')
                payment_record.payment_details = verify_result
                payment_record.save()


                # TODO
                # Additional logic for AI account activation can go here
                user_ai_account = UserAIAccount.objects.create(
                        user=payment_record.user,
                        ai_product=payment_record.product,
                        username='generated_username',  # Replace with your logic to generate a username
                        password='generated_password',  # Replace with your logic to generate a password
                        instructions='Instructions for how to use the AI account'  # Provide appropriate instructions
                    )

            else:
                # Update the payment record with the failure status
                payment_record.status = 'FAILED'
                payment_record.error_message = verify_result.get('message')
                payment_record.save()
                return JsonResponse({"error": "Payment verification failed"}, status=400)

            # Redirect to the AI account purchase success page
            return HttpResponseRedirect(reverse('ai_account_purchase_success', args=[payment_record.id]))
        else:
            return JsonResponse({"error": "Failed to verify payment"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PaymentRecord, AIProduct  # Import the correct models

@login_required
def ai_account_purchase_success(request, payment_record_id):
    # Retrieve the payment record and the associated AI account product
    payment_record = get_object_or_404(PaymentRecord, id=payment_record_id, user=request.user, product__isnull=False)
    ai_account = get_object_or_404(AIProduct, id=payment_record.product.id)

    # Check the payment status
    if payment_record.status != 'SUCCESS':
        messages.error(request, "There was a problem with your payment. Please contact support.")
        return redirect('ai_product_detail', slug=ai_account.slug)

    # Format the date and price
    order_number = payment_record.id
    order_date = payment_record.created_at.strftime('%Y/%m/%d')
    final_price = "{:,.2f}".format(payment_record.amount_paid)
    payment_method = payment_record.payment_method  # Adjust according to your payment method field

    # Prepare the context
    context = {
        'ai_account': ai_account,
        'order_number': order_number,
        'order_date': order_date,
        'final_price': final_price,
        'payment_method': payment_method,
        'message': 'Thank you for purchasing the AI account!',
    }

    # Render the success template (you will provide the template name later)
    return render(request, 'sharifgpt_website/ai_account_order_success.html', context)





from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def accounts_page(request):
    # Retrieve the AI accounts associated with the current user
    user_ai_accounts = request.user.user_ai_accounts.all()

    context = {
        'user_ai_accounts': user_ai_accounts,
    }
    
    return render(request, 'sharifgpt_website/accounts-page.html', context)






from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

def confirm_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            # Set phone verification to false
            user.is_phone_verified = False
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # Redirect to the password reset function with user's ID
            return redirect('password_reset')
        except User.DoesNotExist:
            return HttpResponse('This email does not exist in our records.')
            
    return render(request, 'sharifgpt_website/email_input.html')
