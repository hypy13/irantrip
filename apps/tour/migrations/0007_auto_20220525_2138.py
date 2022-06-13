# Generated by Django 3.2.6 on 2022-05-25 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0006_alter_tour_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='days',
        ),
        migrations.AddField(
            model_name='tourdays',
            name='tour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tour.tour', verbose_name='tour days'),
        ),
    ]
