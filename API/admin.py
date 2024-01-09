from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Video
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    # Make sure 'username' is included if you want it displayed in the admin list
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff',]
    # Updated fieldsets - make sure to include any additional fields you have added
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    ) 

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


