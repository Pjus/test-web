# Generated by Django 3.2.8 on 2021-10-15 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0006_auto_20211015_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educontents',
            name='upload_files',
            field=models.FileField(blank=True, null=True, upload_to='edu/', verbose_name='파일'),
        ),
    ]