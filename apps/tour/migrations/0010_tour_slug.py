# Generated by Django 3.2.6 on 2022-05-30 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0009_auto_20220529_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, null=True),
        ),
    ]