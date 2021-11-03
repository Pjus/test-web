# Generated by Django 3.2.8 on 2021-11-03 07:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_auto_20211103_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='certitem',
            name='registered_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='등록시간'),
            preserve_default=False,
        ),
    ]
