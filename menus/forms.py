from django import forms
from django.forms import TextInput, Textarea, FileInput, CheckboxInput, Select, NumberInput
from django.utils.translation import gettext_lazy as _

from menus.models import Category, Product


class CategoryMenuForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']
        widgets = {
            'category_name': TextInput(attrs={'class': 'menu-item-title', 'placeholder': "Menu Category Title",
                                              'required': True}),
            'description': Textarea(attrs={'class': 'menu-item-desc', 'placeholder': 'Category Description'}),
        }
        error_messages = {
            'category_name': {
                'required': _("This field is required"),
            },
            'description': {
                'required': _("This field is required"),
            }
        }
        labels = {
            "category_name": "Menu Name *",
            "description": "Description",
        }


class ProductMenuForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'product_name', 'description', 'price', 'picture', 'is_available']
        widgets = {
            'category': Select(attrs={'class': 'chosen-select', 'placeholder': "Product title",
                                      'required': True}),
            'product_name': TextInput(attrs={'class': 'menu-item-title', 'placeholder': "Product title",
                                             'required': True}),
            'description': Textarea(attrs={'class': 'menu-item-desc', 'placeholder': 'Product Description',
                                           'cols': 20, 'rows': 5}),
            'price': NumberInput(attrs={'class': 'menu-item-title', 'placeholder': "Product price",
                                        'required': True}),
            'picture': FileInput(attrs={'class': 'inputfile inputfile-1 foodbakery-dev-gallery-uploader',
                                        'style': 'display:none',
                                        'onchange': 'previewLicense(event);'}),
            'is_available': CheckboxInput(attrs={'class': 'menu-item-title', 'placeholder': "Menu Category Title",
                                                 'required': True}),
        }
        error_messages = {
            'product_name': {
                'required': _("This field is required"),
            },
            'description': {
                'required': _("This field is required"),
            },
            'price': {
                'required': _("This field is required"),
            }
        }
        labels = {
            "category": "Restaurant Menu Category *",
            "product_name": "Product Name",
            "description": "Description",
            "price": "Price",
            "picture": "Product Image",
            "is_available": "Is Available",
        }
