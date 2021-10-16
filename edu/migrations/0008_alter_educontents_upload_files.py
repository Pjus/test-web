# Generated by Django 3.2.8 on 2021-10-15 09:47

from django.db import migrations, models
import edu.models


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0007_alter_educontents_upload_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educontents',
            name='upload_files',
            field=models.FileField(blank=True, null=True, upload_to=edu.models.get_file_path, verbose_name='파일'),
        ),
    ]