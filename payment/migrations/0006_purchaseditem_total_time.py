# Generated by Django 3.2.8 on 2021-11-01 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_alter_purchaseditem_stayedtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseditem',
            name='total_time',
            field=models.CharField(default='', max_length=128, null=True, verbose_name='총머문시간'),
        ),
    ]
