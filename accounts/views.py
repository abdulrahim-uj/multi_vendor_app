from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.utils.http import urlsafe_base64_decode
from izitoast.functions import izitoast

from accounts.decorators import check_role_customer
from accounts.decorators import check_role_vendor
from accounts.forms import UserForm
from accounts.models import User
from accounts.models import UserProfile
from accounts.utils import detect_user
from accounts.utils import send_verification_email
from main.functions import get_auto_id
from vendors.forms import VendorForm
from vendors.models import Vendor


def register_user(request):
    # Check user is already signed in or not
    if request.user.is_authenticated:
        message = "You are already logged in!"
        diversify = {
            "position": "topRight",
            "transition_in": "flipInX",
            "transition_out": "flipOutX",
            "time_out": 4000,
        }
        izitoast(request=request, model="info", message=message, diversify=diversify)
        return redirect('accounts:getMyPanel')
    # Check the request method is POST --> Then
    elif request.method == 'POST':
        form = UserForm(request.POST)
        # If form is valid --> Then
        if form.is_valid():
            # CREATE USER USING THE FORM
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            # CREATE USER USING create_user METHOD [from .models UserManager.create_user]
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email_id = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=firstname, last_name=lastname,
                                            username=username, email=email_id,
                                            password=password)
            user.role = User.CUSTOMER
            user.save()
            # SEND VERIFICATION EMAIL
            email_subject = "Activate Your Account"
            email_template = "accounts/emails/account-verification-email.html"
            send_verification_email(request, user, email_subject, email_template)
            message = {
                'raw': [
                    {
                        'tag': "success",
                        'item': "Your account has been registered successfully!"
                    },
                    {
                        'tag': "info",
                        'item': "Please check registered email to activate account."
                    }
                ]
            }
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request, "success", message, diversify)
            return redirect('accounts:registerUser')
        # form is not valid --> Then
        else:
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 6000,
            }
            izitoast(request, "form-error", form.errors, diversify)
    # Request.method is GET --> Then
    else:
        form = UserForm()
    context = {
        "title": "User Registration",
        "form": form,
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
        "growl": False,
        "fliters": False,
        "modernizer": False,
        "ie8and9": False,
        "match_height": False,
        "masonry": False,
        "skills_progress": False,
        "wow": False,
    }
    return render(request, "accounts/register-user.html", context=context)


def register_vendor(request):
    # User is signed in --> then
    if request.user.is_authenticated:
        message = "You are already logged in!"
        diversify = {
            "position": "topRight",
            "transition_in": "flipInX",
            "transition_out": "flipOutX",
            "time_out": 4000,
        }
        izitoast(request=request, model="info", message=message, diversify=diversify)
        return redirect('accounts:getMyPanel')
    # POST request.method
    elif request.method == "POST":
        u_form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        # Two forms are valid --> then
        if u_form.is_valid() and v_form.is_valid():
            firstname = u_form.cleaned_data['first_name']
            lastname = u_form.cleaned_data['last_name']
            username = u_form.cleaned_data['username']
            email_id = u_form.cleaned_data['email']
            password = u_form.cleaned_data['password']
            user = User.objects.create_user(first_name=firstname, last_name=lastname,
                                            username=username, email=email_id,
                                            password=password)
            user.role = User.VENDOR
            user.save()
            # Get and assign userprofile pk to a variable
            user_profile_key = UserProfile.objects.get(user=user)

            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.slug = slugify(vendor_name)
            vendor.user_profile = user_profile_key
            vendor.auto_id = get_auto_id(Vendor)
            vendor.creator = user
            vendor.updater = user
            vendor.save()

            # SEND VERIFICATION EMAIL
            email_subject = "Activate Your Account"
            email_template = "accounts/emails/account-verification-email.html"
            send_verification_email(request, user, email_subject, email_template)
            message = {
                'raw': [
                    {
                        'tag': "success",
                        'item': "Your account has been registered successfully!"
                    },
                    {
                        'tag': "info",
                        'item': "Please check registered email to activate account."
                    },
                    {
                        'tag': "warning",
                        'item': "Be patient, Admin will verify your license to approve."
                    }
                ]
            }
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request, "success", message, diversify)
            return redirect('accounts:registerVendor')
        # form is not valid --> Then
        else:
            combined_errors = str(u_form.errors) + str(v_form.errors)
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request, "form-error", combined_errors, diversify)
    # GET request.method
    else:
        u_form = UserForm()
        v_form = VendorForm()
    context = {
        "title": "Vendor Registration",
        "user_form": u_form,
        "vendor_form": v_form,
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
        "growl": False,
        "fliters": False,
        "modernizer": False,
        "ie8and9": False,
        "match_height": False,
        "masonry": False,
        "skills_progress": False,
        "wow": False,

        'file_input': True,
    }
    return render(request, "accounts/register-vendor.html", context=context)


def activate(request, uidb64, token):
    # ACTIVATE THE USER BY SETTING THE is_activate = True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        message = "Your account has been successfully activated!"
        diversify = {
            "position": "topRight",
            "transition_in": "flipInX",
            "transition_out": "flipOutX",
            "time_out": 4000,
        }
        izitoast(request, "success", message, diversify)
        return redirect('accounts:getMyPanel')
    else:
        message = "Invalid activation link!"
        diversify = {
            "position": "topRight",
            "transition_in": "flipInX",
            "transition_out": "flipOutX",
            "time_out": 4000,
        }
        izitoast(request, "danger", message, diversify)
        return redirect('accounts:getMyPanel')


def log_in(request):
    # Check user is already signed in or not
    if request.user.is_authenticated:
        message = "You are already logged in!"
        diversify = {
            "position": "topRight",
            "transition_in": "flipInX",
            "transition_out": "flipOutX",
            "time_out": 4000,
        }
        izitoast(request=request, model="info", message=message, diversify=diversify)
        return redirect('accounts:getMyPanel')
    elif request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            message = "You are successfully logged in!"
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request, "success", message, diversify)
            return redirect('accounts:getMyPanel')
        else:
            message = "Invalid login credentials!"
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request=request, model="danger", message=message, diversify=diversify)
            return redirect('accounts:signIn')
    else:
        pass
    context = {
        "title": "Authentication",
        # "form": ,
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
        "growl": False,
        "fliters": False,
        "modernizer": False,
        "ie8and9": False,
        "match_height": False,
        "masonry": False,
        "skills_progress": False,
        "wow": False,
    }
    return render(request, "accounts/authentication.html", context=context)


def log_out(request):
    auth.logout(request)
    message = "You are successfully logged out!"
    diversify = {
        "position": "topRight",
        "transition_in": "flipInX",
        "transition_out": "flipOutX",
        "time_out": 4000,
    }
    izitoast(request=request, model="success", message=message, diversify=diversify)
    return redirect('accounts:signIn')


@login_required(login_url='accounts:signIn')
def my_account(request):
    user = request.user
    url_redirect = detect_user(user)
    return redirect(url_redirect)


@login_required(login_url='accounts:signIn')
@user_passes_test(check_role_customer)
def user_dashboard(request):
    context = {
        "title": "Dashboard",
        "is_active_dashboard": True,
        # "form": ,
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
        "growl": False,
        "fliters": False,
        "modernizer": False,
        "ie8and9": False,
        "match_height": False,
        "masonry": False,
        "skills_progress": False,
        "wow": False,
    }
    return render(request, "accounts/user-dashboard.html", context=context)


@login_required(login_url='accounts:signIn')
@user_passes_test(check_role_vendor)
def vendor_dashboard(request):
    context = {
        "title": "Dashboard",
        'is_active_dashboard': True,
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
    }
    return render(request, "accounts/vendor-dashboard.html", context=context)


def forgot_password(request):
    if request.method == 'POST':
        email_id = request.POST.get('user_email')
        if User.objects.filter(email=email_id).exists():
            user = User.objects.get(email__exact=email_id)
            # SEND RESET PASSWORD EMAIL
            email_subject = "Reset Your Password"
            email_template = "accounts/emails/reset-password-email.html"
            send_verification_email(request, user, email_subject, email_template)
            message = "Password reset link has been send to your email address!"
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request=request, model="info", message=message, diversify=diversify)
            return redirect('accounts:signIn')
        else:
            message = "Account does not exist!"
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request=request, model="danger", message=message, diversify=diversify)
            return redirect('accounts:forgotPassword')

    context = {
        "title": "Password Forgot",
        # "form": ,
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
        "growl": False,
        "fliters": False,
        "modernizer": False,
        "ie8and9": False,
        "match_height": False,
        "masonry": False,
        "skills_progress": False,
        "wow": False,
    }
    return render(request, 'accounts/forgot-password.html', context=context)


def reset_password_validate(request, uidb64, token):
    # validating the user by token and pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        message = "Please reset your password!"
        diversify = {
            "position": "topRight",
            "transition_in": "flipInX",
            "transition_out": "flipOutX",
            "time_out": 4000,
        }
        izitoast(request=request, model="info", message=message, diversify=diversify)
        return redirect('accounts:resetPassword')
    else:
        message = "This link has been expired!"
        diversify = {
            "position": "topRight",
            "transition_in": "flipInX",
            "transition_out": "flipOutX",
            "time_out": 4000,
        }
        izitoast(request=request, model="warning", message=message, diversify=diversify)
        return redirect('accounts:getMyPanel')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        if password == confirm:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            message = {
                'raw': [
                    {
                        'tag': "success",
                        'item': "Password reset successfully!"
                    },
                    {
                        'tag': "info",
                        'item': "Please login to your account!"
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
            return redirect('accounts:signIn')
        else:
            message = "Password do not match!"
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request=request, model="danger", message=message, diversify=diversify)
            return redirect('accounts:resetPassword')
    else:
        pass
    context = {
        "title": "Password Reset",
        # "form": ,
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
        "growl": False,
        "fliters": False,
        "modernizer": False,
        "ie8and9": False,
        "match_height": False,
        "masonry": False,
        "skills_progress": False,
        "wow": False,
    }
    return render(request, "accounts/reset-password.html", context=context)
