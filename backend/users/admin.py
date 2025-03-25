from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Import your custom User model

class CustomUserAdmin(UserAdmin):
    model = User

    # Fields to be displayed in the Django Admin list view
    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name', 'bio', 
        'profile_picture_url', 'date_of_birth', 'course_name', 'graduation_year', 
        'country', 'created_at', 'updated_at'
    )

    # Fields that can be searched
    search_fields = ('email', 'username', 'first_name', 'last_name', 'country')

    # Fields that can be edited inline
    fieldsets = (
        ('Basic Info', {'fields': ('email', 'username', 'password')}),
        ('Personal Details', {'fields': ('first_name', 'last_name', 'bio', 'profile_picture_url', 'date_of_birth')}),
        ('Education', {'fields': ('course_name', 'graduation_year')}),
        ('Location', {'fields': ('country',)}),
        ('Important Dates', {'fields': ('created_at', 'updated_at')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    readonly_fields = ('created_at', 'updated_at')  # Prevents changes to these fields

    # Fields for adding a new user
    add_fieldsets = (
        ('Required Information', {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
        ),
        ('Optional Fields', {
            'fields': ('first_name', 'last_name', 'bio', 'profile_picture_url', 'date_of_birth', 
                       'course_name', 'graduation_year', 'country')}
        ),
    )

admin.site.register(User, CustomUserAdmin)