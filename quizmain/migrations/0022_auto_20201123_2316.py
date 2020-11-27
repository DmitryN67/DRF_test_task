# Generated by Django 2.2.10 on 2020-11-23 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizmain', '0021_remove_answer_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='choices',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='choice_answer', to='quizmain.Choice', verbose_name='Варианты'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='question_answer', to='quizmain.Question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='user_id',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choice', to='quizmain.Question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='quizmain.Quiz', verbose_name='Опрос'),
        ),
    ]
