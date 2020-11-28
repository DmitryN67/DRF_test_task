# Generated by Django 2.2.10 on 2020-11-27 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizmain', '0028_auto_20201127_0918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='choices',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='йгуыешщты', to='quizmain.Choice', verbose_name='Варианты'),
            preserve_default=False,
        ),
    ]