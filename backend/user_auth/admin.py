from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'graduation_year', 'created_at', 'course_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'graduation_year', 'country')
    search_fields = ('email', 'first_name', 'last_name', 'course_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'bio', 'profile_picture_url',
                'date_of_birth', 'course_name', 'graduation_year', 'country'
            )
        }),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )