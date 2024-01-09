from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db.models import Sum

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False)  # Added username field
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Added username to required fields

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username  # Changed to return username

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.username  # Return username if full name is not available

    def get_short_name(self):
        return self.first_name if self.first_name else self.username  # Return username if first name is not available

    # Include any additional methods you may need






from django.db import models
from django.utils import timezone

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    profile = models.TextField()

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
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)
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
