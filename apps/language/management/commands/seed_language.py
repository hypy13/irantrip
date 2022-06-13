from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.apps.registry import apps


class Command(BaseCommand):
    help = (
        "feed database with languages \n"
        "usage: python manage.py feed_language\n"
    )

    def handle(self, **options):
        seed_file = apps.get_app_config('dj_language').path + '/data/languages_seed.json'
        call_command('loaddata', seed_file)
