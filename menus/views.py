from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from izitoast.functions import izitoast

from accounts.decorators import check_role_vendor
from main.functions import get_auto_id
from menus.forms import CategoryMenuForm, ProductMenuForm
from menus.models import Category, Product
from vendors.views import get_vendor


@login_required(login_url='accounts:signIn')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor, is_deleted=False)
    products = Product.objects.filter(vendor=vendor)

    category_form = CategoryMenuForm()
    product_form = ProductMenuForm()
    # MODIFY FORMS
    product_form.fields['category'].queryset = Category.objects.filter(vendor=vendor)
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


@login_required(login_url='accounts:signIn')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == "POST":
        form = CategoryMenuForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.auto_id = get_auto_id(Category)
            category.vendor = get_vendor(request)
            category.creator = request.user
            category.updater = request.user
            category.slug = slugify(category_name)
            form.save()
            message = "Category " + category_name + " successfully created."
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request=request, model="success", message=message, diversify=diversify)
            return redirect('menus:menuBuilder')
        else:
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request, "form-error", form.errors, diversify)
            return redirect('menus:menuBuilder')


@login_required(login_url='accounts:signIn')
@user_passes_test(check_role_vendor)
def edit_category(request, pk):
    instance = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryMenuForm(request.POST, instance=instance)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.updater = request.user
            category.slug = slugify(category_name)
            form.save()
            message = "Category " + category_name + " successfully updated."
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request=request, model="success", message=message, diversify=diversify)
            return redirect('menus:menuBuilder')
        else:
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request, "form-error", form.errors, diversify)
            return redirect('menus:menuBuilder')


@login_required(login_url='accounts:signIn')
@user_passes_test(check_role_vendor)
def delete_category(request, pk):
    # Category.objects.filter(pk=pk).update(is_deleted=True)
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    diversify = {
        "position": "topRight",
        "transition_in": "flipInX",
        "transition_out": "flipOutX",
        "time_out": 4000,
    }
    izitoast(request=request, model="success", message="Category deleted successfully!", diversify=diversify)
    return redirect('menus:menuBuilder')


@login_required(login_url='accounts:signIn')
@user_passes_test(check_role_vendor)
def add_product(request):
    if request.method == "POST":
        form = ProductMenuForm(request.POST, request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            product = form.save(commit=False)
            product.auto_id = get_auto_id(Product)
            product.vendor = get_vendor(request)
            product.creator = request.user
            product.updater = request.user
            product.slug = slugify(product_name)
            form.save()
            message = "Product " + product_name + " successfully created."
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request=request, model="success", message=message, diversify=diversify)
            return redirect('menus:menuBuilder')
        else:
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request, "form-error", form.errors, diversify)
            return redirect('menus:menuBuilder')


@login_required(login_url='accounts:signIn')
@user_passes_test(check_role_vendor)
def edit_product(request, pk):
    instance = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductMenuForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            product = form.save(commit=False)
            product.vendor = get_vendor(request)
            product.updater = request.user
            product.slug = slugify(product_name)
            form.save()
            message = "Product " + product_name + " successfully updated."
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request=request, model="success", message=message, diversify=diversify)
            return redirect('menus:menuBuilder')
        else:
            diversify = {
                "position": "topRight",
                "transition_in": "flipInX",
                "transition_out": "flipOutX",
                "time_out": 4000,
            }
            izitoast(request, "form-error", form.errors, diversify)
            return redirect('menus:menuBuilder')


@login_required(login_url='accounts:signIn')
@user_passes_test(check_role_vendor)
def delete_product(request, pk):
    # Product.objects.filter(pk=pk).update(is_deleted=True)
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    diversify = {
        "position": "topRight",
        "transition_in": "flipInX",
        "transition_out": "flipOutX",
        "time_out": 4000,
    }
    izitoast(request=request, model="success", message="Product deleted successfully!", diversify=diversify)
    return redirect('menus:menuBuilder')
