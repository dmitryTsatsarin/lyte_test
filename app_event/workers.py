import json
import logging
import time

import requests
from django.conf import settings
from rest_framework import serializers

from app_event.models import TicketmasterScrapedRawData, Event

logger = logging.getLogger(__name__)


class ScraperWorker:
    """
    It is a simple realization of scraper

    """

    def __init__(self):
        self.limit = 50
        self.api_key = settings.API_KEY
        self.host = 'https://app.ticketmaster.com'

    def gen_url(self, next_link):
        url = f'{self.host}{next_link}&apikey={self.api_key}'
        return url

    def run(self):

        TicketmasterScrapedRawData.objects.all().delete()  # clear old data

        url = self.gen_url('/discovery/v2/events.json?countryCode=US')

        for item in range(self.limit):
            response = requests.request("GET", url, headers={}, data={})
            if response.ok:
                logger.warning(f'Request is successful ({url})')
                content = response.text
                TicketmasterScrapedRawData.objects.create(content=content, url=url, status_code=response.status_code)

                content_dict = response.json()
                next_link = content_dict['_links']['next']['href']
                url = self.gen_url(next_link)
                time.sleep(0.2)  # it is a simple restriction according documentation. Not more than 5 rq/s
            else:
                logger.warning(f'Request is failed ({url})')
                TicketmasterScrapedRawData.objects.create(content=response.text, url=url, status_code=response.status_code)
                break


class NormalizeWorker:
    """
    Normalize input data
    :return:
    """

    def input_mapper(self, event_raw):
        '''
        Input mapper.
        it hard to use DRF serializer for such complex structure, so easiest way is use custom mapper
        :return:
        '''

        try:
            price_min = event_raw.get('priceRanges', [])[0]['min']
        except IndexError:
            price_min = 0

        try:
            price_max = event_raw.get('priceRanges', [])[0]['max']
        except IndexError:
            price_max = 0

        input_data = dict(
            event_name=event_raw.get('name', ''),
            start_datetime_at=serializers.DateTimeField(format='iso-8601').to_internal_value(event_raw['dates']['start']['dateTime']),
            promoter_name=event_raw.get('promoter', {}).get('name', ''),
            description=event_raw.get('info', ''),
            url=event_raw['url'],
            price_min=price_min,
            price_max=price_max,
            # we don't have finish datetime at this moment :(
        )
        return input_data

    def run(self):
        Event.objects.all().delete()  # clear old data

        for item in TicketmasterScrapedRawData.objects.all().values():
            content_dict = json.loads(item['content'])
            print(content_dict)

            for event_raw in content_dict['_embedded']['events']:
                input_data = self.input_mapper(event_raw)
                Event.objects.create(**input_data)
