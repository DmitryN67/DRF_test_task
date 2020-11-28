# Generated by Django 2.2.10 on 2020-11-23 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizmain', '0019_auto_20201123_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='choices', to='quizmain.Choice'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='question', to='quizmain.Question', verbose_name='Вопрос'),
        ),
    ]