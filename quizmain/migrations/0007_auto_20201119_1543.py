# Generated by Django 2.2.10 on 2020-11-19 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizmain', '0006_auto_20201119_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='date_start',
            field=models.DateField(editable=False, verbose_name='Дата старта'),
        ),
    ]