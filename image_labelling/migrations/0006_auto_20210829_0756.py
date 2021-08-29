# Generated by Django 3.2.6 on 2021-08-29 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_labelling', '0005_auto_20210829_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterUniqueTogether(
            name='image',
            unique_together={('integrity',)},
        ),
    ]
