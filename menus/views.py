from django.shortcuts import render

from menus.forms import CategoryMenuForm, ProductMenuForm
from menus.models import Category, Product
from vendors.models import Vendor


def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor, is_deleted=False)
    products = Product.objects.filter(vendor=vendor)

    category_form = CategoryMenuForm()
    product_form = ProductMenuForm()
    context = {
        "title": "Profile",
        "app_title": "Online Food App",
        'is_active_menu_builder': True,
        # CSS
        "google_fonts": True,
        "bootstrap": True,
        "bootstrap_theme": True,
        "icon_moon": True,
        "swiper": True,  # For Dropdown menu
        "style_theme": True,
        "system_food_backery": True,
        "colors": True,
        "widgets": True,
        "responsive": True,
        "bootstrap_datepicker": False,  #
        "bootstrap_slider": False,  #
        "woo_commerce": False,  #
        "pretty_photo": False,  #
        "animate": False,  #
        "chosen": False,  #
        "rtl": False,  #
        # JS
        "ajax1112": True,
        "counter": True,
        "fitvids": True,
        "functions": True,
        "growl": False,
        "fliters": False,
        "modernizer": False,
        "ie8and9": False,
        "match_height": False,
        "masonry": False,
        "skills_progress": False,
        "wow": False,

        "auto_fill_location": False,
        "preview_profile_picture": False,
        "preview_cover_photo": False,
        "preview_license": True,
        "preview_product_picture": True,

        "categories": categories,
        "products": products,
        "form_category": category_form,
        "form_product": product_form,
    }
    return render(request, 'menus/menu-builder.html', context)
