from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'username', 'role',
                    'is_admin', 'is_staff', 'is_superadmin', 'is_active', 'is_deleted',
                    'phone_number', 'date_joined', 'last_login', 'created_date', 'modified_date')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)


class UserProfileAdminView(admin.ModelAdmin):
    list_display = ('id', 'auto_id', 'user', 'profile_picture', 'cover_photo', 'address',
                    'country', 'state', 'city', 'pin_code',
                    'latitude', 'longitude', 'creator', 'updater', 'created_at', 'modified_at',
                    'is_deleted')


admin.site.register(UserProfile, UserProfileAdminView)
