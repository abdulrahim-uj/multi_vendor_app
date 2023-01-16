from django.urls import path

from . import views

app_name = "menus"

urlpatterns = [
    path('', views.menu_builder, name="menuBuilder"),

    path('category/add-category/', views.add_category, name="addCategory"),
    path('category/edit-category/<uuid:pk>/', views.edit_category, name="editCategory"),
    path('category/delete-category/<uuid:pk>/', views.delete_category, name="deleteCategory"),

    path('product/add-product/', views.add_product, name="addProduct"),
    path('product/edit-product/<uuid:pk>/', views.edit_product, name="editProduct"),
    path('product/delete-product/<uuid:pk>/', views.delete_product, name="deleteProduct"),
]
