from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.my_account, name='initial_getMyPanel'),

    path('register-user/', views.register_user, name="registerUser"),
    path('register-vendor/', views.register_vendor, name="registerVendor"),

    path('boot-up/', views.log_in, name="signIn"),
    path('shut-off/', views.log_out, name="signOut"),
    path('my-panel/', views.my_account, name="getMyPanel"),
    path('user-control-panel/', views.user_dashboard, name="userControlPanel"),
    path('vendor-control-panel/', views.vendor_dashboard, name="vendorControlPanel"),

    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('forgot-password/', views.forgot_password, name="forgotPassword"),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate,
         name="resetPasswordValidate"),
    path('reset-password/', views.reset_password, name="resetPassword"),
]
