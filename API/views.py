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
            user = request.user if request.user.is_authenticated else None

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

def send_verification_message(receptor, param1, apikey="2e878d2300e86cbb3fd9e7e7b7d95f3cf0dba3274e70cbeeea17f1a82345163b", template="sharifgpt"):
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

@login_required
def user_dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    courses = [enrollment.course for enrollment in enrollments]
    context = {'courses': courses}
    return render(request, 'sharifgpt_website/dshb-bookmarks.html', context)





from django.shortcuts import render, get_object_or_404
from .models import Event

def event_detail_view(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'event_detail.html', {'event': event})




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

    return render(request, 'checkout-events.html', {'event': event})







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
