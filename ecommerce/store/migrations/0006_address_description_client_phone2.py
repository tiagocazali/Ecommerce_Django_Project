# Generated by Django 5.0.4 on 2024-05-11 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_color_alter_stockitem_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='phone2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
