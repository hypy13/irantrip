# Generated by Django 4.0.4 on 2022-04-25 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('code', models.CharField(max_length=2, unique=True, verbose_name='code')),
                ('status', models.BooleanField(default=False, verbose_name='status')),
                ('countries', models.JSONField(verbose_name='countries')),
            ],
        ),
    ]
