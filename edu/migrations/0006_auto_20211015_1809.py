# Generated by Django 3.2.8 on 2021-10-15 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0005_educontents_upload_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='educontents',
            name='upload_images',
        ),
        migrations.AlterField(
            model_name='educontents',
            name='upload_files',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='파일'),
        ),
    ]
