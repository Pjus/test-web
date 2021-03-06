# Generated by Django 3.2.8 on 2021-10-15 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cert', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certification',
            name='writer',
        ),
        migrations.AddField(
            model_name='certification',
            name='title',
            field=models.CharField(default='', max_length=128, verbose_name='제목'),
        ),
        migrations.AddField(
            model_name='certification',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='사용자'),
        ),
    ]
