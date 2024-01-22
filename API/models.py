from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db.models import Sum




from django.utils.text import slugify
from django.db import models
from django.conf import settings
from django.utils.text import slugify

from django.db import models

class EventCategory(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0, help_text="Used to determine the order of categories")

    class Meta:
        ordering = ['order', 'title']  # Default ordering

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=False)
    category = models.ForeignKey(EventCategory, related_name='events', on_delete=models.CASCADE, null= True)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    speakers = models.ManyToManyField('Speaker', related_name='events')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    image_url = models.URLField(max_length=1024, blank=True, null=True)  # URL field to store the image link



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s booking for {self.event}"
class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone_number:
            raise ValueError('Users must have a phone number')

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_expires = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self):
        return self.first_name





from django.db import models

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    profile = models.TextField()
    image_url = models.URLField(blank=True, null=True)  # Optional: URL to the instructor's image
    resume = models.TextField(blank=True, null=True)  # Add a resume field

    def total_students(self):
        # Assuming each course has an 'enrollment_count' field
        return sum([course.enrollment_count for course in self.course_set.all()])

    def __str__(self):
        return self.name







class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Course(models.Model):
    course_id = models.CharField(max_length=100, unique=True, primary_key=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    STATUS_CHOICES = [
        ('new', 'New'),
        ('popular', 'Popular'),
        ('best_selling', 'Best Selling'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=15, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    language = models.CharField(max_length=50)
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    duration = models.CharField(max_length=100)
    certificate = models.BooleanField(default=False)
    update_policy = models.TextField()
    enrollment_count = models.PositiveIntegerField(default=0)
    rating = models.FloatField(null=True, blank=True)
    last_updated = models.DateField(default=timezone.now)
    prerequisites = models.TextField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, blank=True, null=True)
    video_thumbnail_url = models.URLField(max_length=1024, blank=True, null=True)
    video_url = models.URLField(max_length=1024, blank=True, null=True)
    facebook_link = models.URLField(max_length=1024, blank=True, null=True)
    twitter_link = models.URLField(max_length=1024, blank=True, null=True)
    instagram_link = models.URLField(max_length=1024, blank=True, null=True)
    linkedin_link = models.URLField(max_length=1024, blank=True, null=True)
    duration_icon_url = models.URLField(max_length=1024, blank=True, null=True)
    level_icon_url = models.URLField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)  # e.g., "30 minutes"

    def total_duration(self):
        return self.videos.aggregate(Sum('duration'))['duration__sum'] or 0


    def __str__(self):
        return f'{self.course.title} - {self.title}'

class Review(models.Model):
    course = models.ForeignKey(Course, related_name='reviews', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)  # or link to a User model
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f'{self.course.title} Review by {self.author}'

# You can add more models like 'RelatedCourses' if needed



class Video(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()  # URL to the video content
    duration = models.DurationField()  # Duration of the video

    def __str__(self):
        return self.title




from django.db import models
from django.conf import settings
from .models import Course

class PaymentStatus(models.TextChoices):
    INITIATED = 'initiated', 'Initiated'
    FAILED = 'failed', 'Failed'
    SUCCESS = 'success', 'Success'












from django.db import models
from django.conf import settings

class Payment(models.Model):
    track_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    success = models.BooleanField(default=False)
    status = models.IntegerField()
    paid_at = models.DateTimeField(blank=True, null=True)
    card_number = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ref_number = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    result_code = models.IntegerField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment {self.track_id} - {('Success' if self.success else 'Failed')}"




















class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # ... any other fields like enrollment date, status, etc.



from django.contrib import admin
from .models import Enrollment

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')

admin.site.register(Enrollment, EnrollmentAdmin)



from django.db import models
from django.utils import timezone

class Speaker(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='speakers' , null=True,blank=True)  # Make sure to have Pillow installed
    image_url = models.URLField(max_length=200 ,null= True)
    def __str__(self):
        return self.name






from django.db import models
from django.utils import timezone

class EventPaymentRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)  # Adjust the max_length as needed
    payment_method = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    track_id = models.CharField(max_length=100, blank=True, null=True)
    payment_message = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}'s payment for {self.event}"






from django.db import models
from django.utils.text import slugify
from django.conf import settings

# Existing imports...

class AIProduct(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='ai_products', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1024, blank=True, null=True)
    slug = models.SlugField(unique=True)
    image_url_1 = models.URLField(max_length=1024, blank=True, null=True)
    image_url_2 = models.URLField(max_length=1024, blank=True, null=True)
    image_url_3 = models.URLField(max_length=1024, blank=True, null=True)
    image_url_4 = models.URLField(max_length=1024, blank=True, null=True)
    # Add more fields as needed
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class AIProductFeature(models.Model):
    product = models.ForeignKey(AIProduct, related_name='features', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.product.name}"

class AIProductReview(models.Model):
    product = models.ForeignKey(AIProduct, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.product}"


# /path/to/models.py

from django.db import models

class AIProductImage(models.Model):
    product = models.ForeignKey(AIProduct, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name} ({self.alt_text})"



from django.db import models
from django.conf import settings
from .models import Course, PaymentStatus

class PaymentRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)

    product = models.ForeignKey(AIProduct, on_delete=models.CASCADE, null=True, blank=True)

    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.INITIATED)
    transaction_id = models.CharField(max_length=120, blank=True, null=True)  # New field for transaction ID
    payment_method = models.CharField(max_length=50, blank=True, null=True)  # New field for payment method
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # New field for amount paid
    error_message = models.TextField(blank=True)
    payment_details = models.JSONField(blank=True, null=True)  # New field for storing JSON payment details
    created_at = models.DateTimeField(auto_now_add=True)
    track_id = models.CharField(max_length=120, blank=True, null=True)  # To store the trackId from the payment gateway
    payment_message = models.CharField(max_length=255, blank=True, null=True)  # To store the payment message


    def __str__(self):
        if self.course:
            return f"{self.user}'s payment for {self.course.title} - {self.status} ({self.transaction_id})"
        elif self.event:
            return f"{self.user}'s payment for {self.event.title} - {self.status} ({self.transaction_id})"
        else:
            return f"{self.user}'s payment - {self.status} ({self.transaction_id})"
    











from django.conf import settings
from django.db import models
from .models import AIProduct

class UserAIAccount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_ai_accounts'
    )
    ai_product = models.ForeignKey(
        AIProduct,
        on_delete=models.CASCADE,
        related_name='user_accounts'
    )
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    instructions = models.TextField()

    # ... any other fields you might need ...
    
    def __str__(self):
        return f"{self.user.email}'s account for {self.ai_product.name}"
