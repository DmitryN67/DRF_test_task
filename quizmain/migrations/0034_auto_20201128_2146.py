# Generated by Django 2.2.10 on 2020-11-28 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizmain', '0033_auto_20201128_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_text',
            field=models.CharField(blank=True, max_length=50, verbose_name='Ответ'),
        ),
    ]