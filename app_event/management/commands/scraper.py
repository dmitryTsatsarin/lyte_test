from django.core.management.base import BaseCommand

from app_event.workers import ScraperWorker


class Command(BaseCommand):

    def handle(self, *args, **options):
        ScraperWorker().run()
