from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):

        call_command('loaddata', 'main/fixtures/default_rate.json', verbosity=0)
        call_command('loaddata', 'main/fixtures/admin_user.json', verbosity=0)
