from django.db import models
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField

from main.models import BaseModel
from accounts.utils import send_notification_email
from accounts.models import User, UserProfile
from main.validators import allow_only_images_validator


class Vendor(BaseModel):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=180)
    vendor_license = VersatileImageField('vendor_license', upload_to='vendors/license/',
                                         validators=[allow_only_images_validator],
                                         blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'vendors_vendor'
        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')
        ordering = ('-created_at', 'vendor_name')

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            if Vendor.objects.filter(pk=self.pk).exists():
                original = Vendor.objects.get(pk=self.pk)
                # UPDATE
                if original.is_approved != self.is_approved:
                    mail_template = "accounts/emails/admin-approval-email.html"
                    context = {
                        'user': self.user,
                        'approved': self.is_approved
                    }
                    if self.is_approved:
                        # SEND NOTIFICATION EMAIL
                        mail_subject = "Congratulations! Your restaurant has been approved."
                        send_notification_email(mail_subject, mail_template, context)
                    else:
                        # SEND NOTIFICATION EMAIL
                        mail_subject = "We are sorry! You are not eligible for publishing your " \
                                       "food menu on our marketplace."
                        send_notification_email(mail_subject, mail_template, context)
                return super(Vendor, self).save(*args, **kwargs)
            else:
                return super(Vendor, self).save(*args, **kwargs)
