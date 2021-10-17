# Generated by Django 3.2.8 on 2021-10-17 11:09

import cart.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('edu', '0014_remove_product_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_date', models.DateTimeField(auto_now_add=True, verbose_name='등록시간')),
                ('cart_id', models.CharField(default=cart.models.random_string, max_length=18)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='구매자')),
            ],
            options={
                'db_table': 'Cart',
                'ordering': ['registered_date'],
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/', verbose_name='이미지')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edu.product')),
            ],
            options={
                'db_table': 'CartItem',
            },
        ),
    ]
