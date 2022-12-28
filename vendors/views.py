import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from izitoast.functions import izitoast
from opencage.geocoder import OpenCageGeocode

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
            message = "Successfully updated!"
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request=request, model="success", message=message, diversify=diversify)
            return redirect('vendors:vendorProfile')
        else:
            combined_errors = str(form_user_profile.errors) + str(form_vendor.errors)
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


def get_lat_long(request):
    search_location = request.GET.get('location')
    try:
        key = settings.OPENCAGE_KEY
        geocoder = OpenCageGeocode(key)

        query = search_location
        result = geocoder.geocode(query)
        # print(result)
        # print(result[0]['geometry']['lat'])
        # print(result[0]['geometry']['lng'])
        # print(result[0]['formatted'])
        # print(result[0]['components']['country_code'])
        # print(result[0]['annotations']['timezone']['name'])
        # print(result[0]['annotations']['currency']['name'])  # + ['symbol', 'iso_code']
        # print(result[0]['components'][
        #           '_type'])  # continent, country, country_code, county, postcode, state, state_code, state_district, village
        #
        # print(result[1]['annotations']['roadinfo']['road'])
        # print(result[1]['components']['neighbourhood'])
        return HttpResponse(json.dumps(result), content_type='application/javascript')
    except:
        message = "Error"
        # return redirect('vendors:vendorProfile')
        return HttpResponse(json.dumps(message), content_type='application/javascript')
