from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Video
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'phone_number', 'first_name', 'last_name', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone_number', 'first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Update this if you want a specific ordering in the admin list view
    ordering = ['email']

admin.site.register(CustomUser, CustomUserAdmin)



from django.contrib import admin
from .models import Course, Instructor, Category, Subcategory, Lesson, Review

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'title', 'instructor', 'category', 'subcategory', 'status', 'enrollment_count', 'rating')
    search_fields = ('title', 'instructor__name')
    list_filter = ('status', 'level', 'language', 'category', 'subcategory')
    date_hierarchy = 'last_updated'

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

class VideoInline(admin.StackedInline):
    model = Video
    extra = 1  # Number of empty forms to display

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration')
    search_fields = ('title', 'course__title')
    inlines = [VideoInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'author', 'rating')
    search_fields = ('course__title', 'author')
    list_filter = ('rating',)





@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'title', 'duration', 'url')
    search_fields = ('title', 'lesson__title')
    list_filter = ('lesson',)




from django.contrib import admin
from .models import PaymentRecord

@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'course__title')




from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('track_id', 'order_id', 'amount', 'status', 'success', 'paid_at')
    search_fields = ('track_id', 'order_id', 'status')
    list_filter = ('status', 'success', 'paid_at')
    readonly_fields = ('track_id', 'order_id', 'amount', 'status', 'success', 'paid_at',
                       'card_number', 'ref_number', 'description', 'result_code', 'message')

    # Optionally, you can add fieldsets for a more organized layout in the admin detail view
    fieldsets = (
        (None, {
            'fields': ('track_id', 'order_id', 'amount', 'status', 'success')
        }),
        ('Payment Details', {
            'fields': ('card_number', 'ref_number', 'description', 'result_code', 'message', 'paid_at')
        }),
    )

    def has_add_permission(self, request, obj=None):
        # Optionally, disable adding new Payments through admin
        return False

admin.site.register(Payment, PaymentAdmin)



from django.contrib import admin
from .models import Event, Booking
from django.utils.text import slugify

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'price', 'discount')
    list_filter = ('date', 'location')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Event, EventAdmin)



class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'quantity', 'total_price', 'purchase_date')
    list_filter = ('purchase_date', 'event')
    search_fields = ('user__email', 'event__title')

admin.site.register(Booking, BookingAdmin)



from django.contrib import admin
from .models import Speaker

class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    search_fields = ('name', 'title')
    list_filter = ('title',)

admin.site.register(Speaker, SpeakerAdmin)

from django.contrib import admin
from .models import EventPaymentRecord

class EventPaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'payment_method', 'amount_paid', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'event__title', 'track_id')
    readonly_fields = ('created_at',)

    # If you want to customize the form displayed when editing/creating a record,
    # you can use the 'fields' attribute.
    # fields = ('user', 'event', 'status', 'payment_method', 'amount_paid', 'track_id', 'payment_message', 'error_message', 'created_at')

    # If you have a lot of records and want to optimize the performance of your admin interface,
    # you can use the 'raw_id_fields' to use an input box instead of a dropdown.
    # raw_id_fields = ('user', 'event',)

admin.site.register(EventPaymentRecord, EventPaymentRecordAdmin)



from django.contrib import admin
from .models import EventCategory

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    ordering = ('order', 'title')  # How items are ordered in the admin list view


from django.contrib import admin
from .models import AIProductImage


from django.contrib import admin
from .models import AIProduct, AIProductFeature, AIProductReview

class AIProductImageInline(admin.TabularInline):
    model = AIProductImage
    extra = 1

class AIProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    search_fields = ['name', 'category__name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [AIProductImageInline]

admin.site.register(AIProduct, AIProductAdmin)

class AIProductFeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'product']
    search_fields = ['name', 'product__name']

admin.site.register(AIProductFeature, AIProductFeatureAdmin)

class AIProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'review_date']
    search_fields = ['product__name', 'user__email']

admin.site.register(AIProductReview, AIProductReviewAdmin)


# /path/to/admin.py

from django.contrib import admin
from .models import UserAIAccount



@admin.register(UserAIAccount)
class UserAIAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'ai_product', 'username', 'password')
    list_filter = ('ai_product',)
    search_fields = ('user__username', 'ai_product__name', 'username')


