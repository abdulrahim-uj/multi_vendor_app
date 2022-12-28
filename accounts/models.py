import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import OneToOneField
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField

from main.models import BaseModel
from main.validators import allow_only_images_validator


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_deleted = False
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = 'accounts_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined', 'username')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
            return user_role
        elif self.role == 2:
            user_role = 'Customer'
            return user_role


class UserProfile(BaseModel):
    user = OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = VersatileImageField('profile_picture',
                                          upload_to="users/profile_pictures/",
                                          validators=[allow_only_images_validator],
                                          blank=True, null=True)
    cover_photo = VersatileImageField('cover_photo', upload_to='users/cover_photos/',
                                      validators=[allow_only_images_validator],
                                      blank=True, null=True, )
    address = models.CharField(max_length=250, blank=True, null=True)
    continent = models.CharField(max_length=128, blank=True, null=True)
    country_code = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    state_code = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    district = models.CharField(max_length=128, blank=True, null=True)
    location_type = models.CharField(max_length=128, blank=True, null=True)
    village = models.CharField(max_length=128, blank=True, null=True)
    county = models.CharField(max_length=128, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    formatted = models.CharField(max_length=128, blank=True, null=True)
    road_info = models.CharField(max_length=128, blank=True, null=True)
    neighbourhood = models.CharField(max_length=128, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'accounts_userprofile'
        verbose_name = _('userprofile')
        verbose_name_plural = _('userprofiles')
        ordering = ('-created_at', 'user')

    def __str__(self):
        return self.user.email

    # Uses to combine two address fields to single
    # def full_address(self):
    #     return f'{self.address_line_1}, {self.address_line_2}'
