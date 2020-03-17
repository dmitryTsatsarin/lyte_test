from django.core.management.base import BaseCommand

from app_event.workers import NormalizeWorker


class Command(BaseCommand):

    def handle(self, *args, **options):
        NormalizeWorker().run()
