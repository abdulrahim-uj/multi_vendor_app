from django.urls import path

from . import views

app_name = "vendors"

urlpatterns = [
    path('', views.initialize_v_profile, name="initialVendorProfile"),
    path('profile/', views.v_profile, name="vendorProfile"),
]
