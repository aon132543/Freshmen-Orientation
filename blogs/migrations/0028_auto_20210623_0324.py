# Generated by Django 3.0.7 on 2021-06-23 03:24

import cropperjs.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0027_auto_20210623_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_bg_pic',
            field=cropperjs.models.CropperImageField(aspectratio=1.7777, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=cropperjs.models.CropperImageField(aspectratio=1.7777, upload_to='images'),
        ),
    ]
