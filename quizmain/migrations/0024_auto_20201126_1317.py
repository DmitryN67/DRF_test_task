# Generated by Django 2.2.10 on 2020-11-26 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizmain', '0023_auto_20201125_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='user',
        ),
        migrations.AddField(
            model_name='answer',
            name='user_id',
            field=models.PositiveIntegerField(default=2),
            preserve_default=False,
        ),
    ]