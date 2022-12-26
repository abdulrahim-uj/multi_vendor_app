from django import forms
from django.forms import FileInput
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _

from . models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
        widgets = {
            'vendor_license': FileInput(attrs={'class': 'inputfile inputfile-1 foodbakery-dev-gallery-uploader',
                                               'style': 'display:none',
                                               'onchange': 'previewLicense(event);'}),
            'vendor_name': TextInput(attrs={'class': 'foodbakery-dev-req-field'}),
        }
        error_messages = {
            'vendor_name': {
                'required': _("This field is required"),
            },
            'vendor_license': {
                'required': _("This field is required"),
            }
        }
        labels = {
            "vendor_name": "Restaurant name *",
            "vendor_license": "Vendor license",
        }
