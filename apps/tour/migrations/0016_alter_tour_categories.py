# Generated by Django 3.2.6 on 2022-05-30 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('tour', '0015_auto_20220530_0242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='categories',
            field=models.ManyToManyField(blank=True, to='categories.Category'),
        ),
    ]
