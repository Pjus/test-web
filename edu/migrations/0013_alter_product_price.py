# Generated by Django 3.2.8 on 2021-10-16 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0012_auto_20211016_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(),
        ),
    ]
