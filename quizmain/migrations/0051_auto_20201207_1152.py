# Generated by Django 2.2.10 on 2020-12-07 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizmain', '0050_auto_20201207_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='session',
            field=models.CharField(max_length=100, verbose_name='Сессия'),
        ),
    ]
