# Generated by Django 2.2.10 on 2020-11-26 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizmain', '0025_auto_20201126_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.PositiveIntegerField(),
        ),
    ]
