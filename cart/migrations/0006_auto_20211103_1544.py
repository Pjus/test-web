# Generated by Django 3.2.8 on 2021-11-03 06:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0005_certitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='certitem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='구매자'),
        ),
        migrations.AlterField(
            model_name='certitem',
            name='active',
            field=models.BooleanField(default=True, verbose_name='배송중'),
        ),
    ]