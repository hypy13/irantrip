# Generated by Django 4.0.4 on 2022-04-25 18:03

import apps.language.field
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('language', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('photo', models.ImageField(upload_to='sliders')),
                ('status', models.BooleanField(default=True, verbose_name='status')),
                ('language', apps.language.field.LanguageField(default=69, limit_choices_to={'status': True}, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='language.language', verbose_name='language')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
