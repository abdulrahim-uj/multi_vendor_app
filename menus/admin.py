from django.contrib import admin

from menus.models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name', )}
    list_display = ('id', 'auto_id', 'vendor', 'category_name', 'slug',
                    'creator', 'updater', 'created_at',
                    'modified_at', 'is_deleted')
    list_display_links = ('vendor',)
    # list_editable = ('is_approved', )
    list_per_page = 10
    search_fields = ('category_name', 'vendor__vendor_name')


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name', )}
    list_display = ('id', 'auto_id', 'vendor', 'category', 'product_name', 'slug',
                    'price', 'picture', 'is_available', 'creator',
                    'updater', 'created_at', 'modified_at', 'is_deleted')
    list_display_links = ('vendor', 'category',)
    list_editable = ('is_available', 'price',)
    list_per_page = 10
    search_fields = ('product_name', 'price', 'category__category_name', 'vendor__vendor_name')
    list_filter = ('is_available', )


admin.site.register(Product, ProductAdmin)

