from django import forms
from django.forms import FileInput
from django.forms import TextInput, NumberInput
from django.utils.translation import gettext_lazy as _

from .models import User
from .models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        error_messages = {
            'first_name': {
                'required': _("This field is required"),
            },
            'last_name': {
                'required': _("This field is required"),
            },
            'username': {
                'required': _("This field is required"),
            },
            'email': {
                'required': _("This field is required"),
            },
            'password': {
                'required': _("This field is required"),
            },
        }
        labels = {
            "first_name": "First name",
            "email": "E-mail",
            "password": "Password",
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not  match!")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['creator', 'updater', 'auto_id', 'is_deleted']
        fields = ['profile_picture', 'cover_photo', 'address', 'continent', 'country_code', 'country', 'state_code',
                  'state', 'city', 'district', 'location_type', 'village', 'county', 'pin_code', 'formatted',
                  'road_info', 'neighbourhood', 'latitude', 'longitude']
        widgets = {
            'profile_picture': FileInput(attrs={
                'class': 'foodbakery-dev-gallery-uploader', 'style': 'display:none',
                'onchange': 'previewProfilePicture(event);'}),
            'cover_photo': FileInput(attrs={'class': 'foodbakery-dev-gallery-uploader',
                                            'style': 'display:none',
                                            'onchange': 'previewCoverPhoto(event);'}),
            'address': TextInput(attrs={'required': 'required', 'onfocusout': 'auto_fill_all()'}),
            # 'country': TextInput(),
            # 'state': TextInput(),
            # 'city': TextInput(),
            # 'pin_code': NumberInput(),
            # Normal way to make readonly
            # 'latitude': TextInput(attrs={'class': 'foodbakery-dev-gallery-uploader',
            #                              'readonly': 'readonly'}),
            # 'longitude': TextInput(attrs={'class': 'foodbakery-dev-gallery-uploader',
            #                              'readonly': 'readonly'}),
        }
        labels = {
            'profile_picture': "Upload Logo",
            'cover_photo': "Upload Cover Image",
            'address': "Address",
            'continent': "Continent",
            'country_code': "Country code",
            'country': "Country",
            'state_code': "State code",
            'state': "State",
            'city': "City",
            'district': "District",
            'location_type': "Location type",
            'village': "Village",
            'county': "Circle",
            'pin_code': "Zip Code",
            'formatted': "Long Address",
            'road_info': "Road info",
            'neighbourhood': "Neighbourhood",
            'latitude': "Latitude",
            'longitude': "Longitude",
        }
        error_messages = {
            'profile_picture': {
                'required': _("This field is required"),
            },
            'cover_photo': {
                'required': _("This field is required"),
            },
            'address': {
                'required': _("This field is required"),
            },
            'country': {
                'required': _("This field is required"),
            },
            'state': {
                'required': _("This field is required"),
            },
            'city': {
                'required': _("This field is required"),
            },
            'pin_code': {
                'required': _("This field is required"),
            },
            'latitude': {
                'required': _("This field is required"),
            },
            'longitude': {
                'required': _("This field is required"),
            },
        }

    # Advanced way to set readonly property
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            # if field in ['continent', 'country_code', 'country', 'state_code', 'state', 'city',
            #              'district', 'location_type', 'village', 'county', 'pin_code', 'formatted',
            #              'road_info', 'neighbourhood', 'latitude', 'longitude']:
            #     self.fields[field].widget.attrs['readonly'] = 'readonly'
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
