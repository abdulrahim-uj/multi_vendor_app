# Generated by Django 4.1.5 on 2023-01-16 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0005_vendor_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='slug',
            field=models.SlugField(max_length=128, unique=True),
        ),
    ]
