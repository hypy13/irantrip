# Generated by Django 3.2.6 on 2022-04-25 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_post_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.IntegerField(choices=[('0', 'Draft'), ('1', 'Publish')], default='0'),
        ),
    ]