# Generated by Django 3.2.6 on 2022-05-25 20:41

import apps.tour.fields.summernote
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0005_auto_20220525_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='content',
            field=apps.tour.fields.summernote.SummernoteField(verbose_name='content'),
        ),
    ]