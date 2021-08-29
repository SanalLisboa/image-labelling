# Generated by Django 3.2.6 on 2021-08-29 05:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('image_labelling', '0003_auto_20210829_0447'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='label',
            unique_together={('user_id', 'image_id', 'label')},
        ),
    ]
