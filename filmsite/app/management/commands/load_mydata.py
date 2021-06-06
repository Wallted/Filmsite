from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        call_command('app_init')
        call_command('loaddata', '../my-data.json')
