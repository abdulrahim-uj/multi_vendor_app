from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404

from menus.models import Category, Product
from vendors.models import Vendor


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        "title": "Marketplace",
        # "form": ,
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

        "vendors": vendors,
        "total_vendors": vendor_count,
    }
    return render(request, 'marketplaces/marketplace.html', context)


def vendor_detail(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)
    # reverse lookup from products to category
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'products',
            queryset=Product.objects.filter(is_available=True)
        )
    )
    context = {
        "title": "Marketplace",
        # "form": ,
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

        "vendor": vendor,
        "categories": categories,
    }
    return render(request, 'marketplaces/vendor-detail.html', context)
