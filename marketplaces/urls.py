from django.urls import path

from . import views

app_name = "marketplaces"

urlpatterns = [
    path('', views.marketplace, name="marketplace"),
    path('<slug:slug>/', views.vendor_detail, name="vendorDetail"),
]
