from django.shortcuts import render
from django.http.response import HttpResponseRedirect  # HttpResponse
from django.urls import reverse


def app(request):
    return HttpResponseRedirect(reverse('beginning'))


def opening(request):
    context = {
        "title": "Dashboard",
        # CSS
        "google_fonts": True,
        "bootstrap": True,
        "bootstrap_theme": True,
        "icon_moon": True,
        "swiper": True, # For Dropdown menu
        "style_theme": True,
        "system_food_backery": True,
        "colors": True,
        "widgets": True,
        "responsive": True,
        "toast": True,
        "bootstrap_datepicker": False,#
        "bootstrap_slider": False,#
        "woo_commerce": False,#
        "pretty_photo": False,#
        "animate": False,#
        "chosen": False,#
        "rtl": False,#
        # JS
        "ajax1112": True,
        "counter": True,
        "fitvids": True,
        "functions": True,
        "message_alert": True,
        "growl": False,
        "fliters": False,
        "modernizer": False,
        "ie8and9": False,
        "match_height": False,
        "masonry": False,
        "skills_progress": False,
        "wow": False,
    }
    return render(request, "main/home.html", context)
