# Generated by Django 2.2.10 on 2020-11-27 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizmain', '0029_auto_20201127_1011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.AddField(
            model_name='quiz',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='quizmain.Question', verbose_name='Опрос'),
            preserve_default=False,
        ),
    ]
