from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        call_command('dumpdata', '-o', 'data.json')
        open("../my-data.json","wb").write(open("data.json").read().encode("utf8"))
        os.remove("data.json")
