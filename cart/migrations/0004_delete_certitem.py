# Generated by Django 3.2.8 on 2021-11-03 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_certitem_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CertItem',
        ),
    ]