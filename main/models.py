import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    creator = models.ForeignKey("accounts.User", blank=True,
                                related_name="creator_%(class)s_objects",
                                on_delete=models.CASCADE)
    updater = models.ForeignKey("accounts.User", blank=True,
                                related_name="updator_%(class)s_objects",
                                on_delete=models.CASCADE)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Mode(models.Model):
    readonly = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)
    down = models.BooleanField(default=False)

    class Meta:
        db_table = 'main_mode'
        verbose_name = _('mode')
        verbose_name_plural = _('modes')
        ordering = ('id',)

    class Admin:
        list_display = ('id', 'readonly', 'maintenance', 'down')

    def __str__(self):
        return str(self.id)


class Visitors(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    latitude = models.CharField(max_length=128)
    longitude = models.CharField(max_length=128)
    formatted = models.CharField(max_length=128)
    country_code = models.CharField(max_length=128)
    time_Zone = models.CharField(max_length=128)
    currency_name = models.CharField(max_length=128)
    location_type = models.CharField(max_length=128)
    continent = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    county = models.CharField(max_length=128)
    post_code = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    state_code = models.CharField(max_length=128)
    district = models.CharField(max_length=128)
    village = models.CharField(max_length=128)
    road_info = models.CharField(max_length=128)
    neighbourhood = models.CharField(max_length=128)

    class Meta:
        db_table = 'main_visitors'
        verbose_name = _('visitor')
        verbose_name_plural = _('visitors')
        ordering = ('-created_at', 'formatted')

    def __str__(self):
        return self.formatted
