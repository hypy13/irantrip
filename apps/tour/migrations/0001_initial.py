# Generated by Django 3.2.6 on 2022-04-25 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('content', models.TextField(verbose_name='content')),
                ('rate', models.PositiveSmallIntegerField(default=5, verbose_name='rate')),
                ('group_max', models.PositiveSmallIntegerField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('geo_points', models.CharField(help_text='seperate points with comma (,) ', max_length=512)),
                ('priority', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='priority')),
                ('status', models.BooleanField(default=True, verbose_name='status')),
                ('categories', models.ManyToManyField(to='categories.Category')),
            ],
            options={
                'verbose_name': 'Tour Package',
                'verbose_name_plural': 'Tour Packages',
                'ordering': ['priority', '-id'],
            },
        ),
        migrations.CreateModel(
            name='TourItinerary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='question')),
                ('content', models.TextField(verbose_name='answer')),
                ('priority', models.IntegerField(blank=True, null=True, verbose_name='priority')),
            ],
            options={
                'ordering': ['priority', '-id'],
            },
        ),
        migrations.CreateModel(
            name='TourPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('photo', models.ImageField(upload_to='tours')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='tour.tour')),
            ],
        ),
    ]
