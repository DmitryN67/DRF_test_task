# Generated by Django 2.2.10 on 2020-11-29 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizmain', '0035_answer_quiz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='quiz',
        ),
        migrations.CreateModel(
            name='Respondent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.ManyToManyField(blank=True, related_name='Ответ', to='quizmain.Answer')),
                ('quiz', models.ManyToManyField(blank=True, related_name='quiz_answer', to='quizmain.Quiz', verbose_name='Опрос')),
            ],
        ),
    ]
