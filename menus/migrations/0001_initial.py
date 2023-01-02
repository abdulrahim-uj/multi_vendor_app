# Generated by Django 4.1.4 on 2022-12-30 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.validators
import uuid
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendors', '0004_alter_vendor_vendor_license'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('auto_id', models.PositiveIntegerField(db_index=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('category_name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(max_length=128, unique=True)),
                ('description', models.TextField(blank=True, max_length=256)),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
                ('updater', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='updator_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendors.vendor')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'menus_category',
                'ordering': ('-created_at', 'category_name'),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('auto_id', models.PositiveIntegerField(db_index=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('product_name', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128, unique=True)),
                ('description', models.TextField(blank=True, max_length=256)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('picture', versatileimagefield.fields.VersatileImageField(upload_to='products/pictures/', validators=[main.validators.allow_only_images_validator], verbose_name='product_picture')),
                ('is_available', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menus.category')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
                ('updater', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='updator_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendors.vendor')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'menus_product',
                'ordering': ('-created_at', 'product_name'),
            },
        ),
    ]
