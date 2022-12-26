from django.contrib import admin

from . models import Vendor


class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'auto_id', 'user', 'user_profile', 'vendor_name',
                    'vendor_license', 'is_approved', 'creator', 'updater', 'created_at',
                    'modified_at', 'is_deleted')
    list_display_links = ('user', 'vendor_name')
    list_editable = ('is_approved', )
    list_per_page = 10


admin.site.register(Vendor, VendorAdmin)
