# Generated by Django 3.2.8 on 2021-10-20 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0011_alter_quizcontents_quiz_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizcontents',
            name='cert',
            field=models.BooleanField(default=False, verbose_name='수료여부'),
        ),
    ]