# Generated by Django 3.0.7 on 2021-06-23 03:45

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0029_auto_20210623_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('profile_pic', '300x300', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
    ]
