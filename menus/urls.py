from django.urls import path

from . import views

app_name = "menus"

urlpatterns = [
    path('', views.menu_builder, name="menuBuilder"),
]
