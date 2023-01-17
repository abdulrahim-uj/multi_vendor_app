from django.db import models
from main.models import BaseModel
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField
from main.validators import allow_only_images_validator


class Category(BaseModel):
    vendor = models.ForeignKey("vendors.Vendor", on_delete=models.CASCADE)
    category_name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
    description = models.TextField(max_length=256, blank=True)

    class Meta:
        db_table = 'menus_category'
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('-created_at', 'category_name')

    def clean(self):
        self.category_name = self.category_name.capitalize()

    def __str__(self):
        return self.category_name


class Product(BaseModel):
    vendor = models.ForeignKey("vendors.Vendor", on_delete=models.CASCADE)
    ''' related_name='products'
        for reverse lookup views...
        related name same as model name in small letters with plural '''
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    description = models.TextField(max_length=256, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = VersatileImageField('product_picture', upload_to='products/pictures/',
                                  validators=[allow_only_images_validator])
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'menus_product'
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ('-created_at', 'product_name')

    def clean(self):
        self.product_name = self.product_name.capitalize()

    def __str__(self):
        return self.product_name
