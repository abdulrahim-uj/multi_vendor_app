from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from izitoast.functions import izitoast

from accounts.decorators import check_role_vendor
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from vendors.forms import VendorForm
from vendors.models import Vendor


@login_required(login_url='accounts:signIn')
@user_passes_test(check_role_vendor)
def initialize_v_profile(request):
    return HttpResponseRedirect(reverse('vendors:vendorProfile'))


@login_required(login_url='accounts:signIn')
@user_passes_test(check_role_vendor)
def v_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        form_user_profile = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        form_vendor = VendorForm(request.POST, request.FILES, instance=vendor)
        if form_user_profile.is_valid() and form_vendor.is_valid():
            form_user_profile.save()
            form_vendor.save()
            message = {
                'raw': [
                    {
                        'tag': "success",
                        'item': "Successfully updated."
                    }
                ]
            }
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request=request, model="success", message=message, diversify=diversify)
            return redirect('vendors:vendorProfile')
        else:
            combined_errors = (form_user_profile.errors + form_vendor.errors)
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request, "form-error", combined_errors, diversify)
    else:
        form_user_profile = UserProfileForm(instance=user_profile)
        form_vendor = VendorForm(instance=vendor)

    context = {
        "title": "Profile",
        "app_title": "Online Food App",
        'is_active_my_restaurant': True,
        'form_user_profile': form_user_profile,
        'form_vendor': form_vendor,
        'user_profile': user_profile,
        'vendor': vendor,
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

        "preview_profile_picture": True,
        "preview_cover_photo": True,
        "preview_license": True,
    }
    return render(request, "vendors/profile.html", context=context)
