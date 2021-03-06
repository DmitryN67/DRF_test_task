# Generated by Django 2.2.10 on 2020-12-03 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sessions', '0001_initial'),
        ('quizmain', '0041_auto_20201203_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='user',
        ),
        migrations.CreateModel(
            name='Respondent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='quiz_respondent', to='quizmain.Quiz', verbose_name='Опрос')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='sessions.Session', verbose_name='Сессия')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='respondent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='respondent_answer', to='quizmain.Respondent', verbose_name='Пользователь'),
        ),
    ]
