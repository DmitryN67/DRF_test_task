# Generated by Django 2.2.10 on 2020-11-23 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizmain', '0016_auto_20201122_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='answer_text',
        ),
        migrations.AddField(
            model_name='answer',
            name='choice',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='quizmain.Choice'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='quizmain.Question'),
        ),
    ]
