import datetime

from rest_framework import status as rest_status

from app_event.factories import EventFactory
from app_event.models import Event
from common.testing import CommonTestCase


class EventTestCase(CommonTestCase):

    def test_get_all_events(self):
        EventFactory.create(
            event_name='tttest',
            start_datetime_at=datetime.datetime.now(),
            promoter_name='test_organizer_name',
            price_min=10.1,
            price_max=100
        )

        EventFactory.create(
            event_name='tttest2',
            start_datetime_at=datetime.datetime.now(),
            promoter_name='test_organizer_name',
            price_min=10.1,
            price_max=100
        )

        response = self.client.get(f'/api/events', format='json')
        content_dict = self.content_to_dict(response.content)
        self.assertEqual(response.status_code, rest_status.HTTP_200_OK)
        self.assertEqual(len(content_dict), 2)

    def test_search_by_name(self):
        EventFactory.create(
            event_name='tttest',
            start_datetime_at=datetime.datetime.now(),
            promoter_name='test_organizer_name',
            price_min=10.1,
            price_max=100
        )

        EventFactory.create(
            event_name='tttest2',
            start_datetime_at=datetime.datetime.now(),
            promoter_name='test_organizer_name',
            price_min=10.1,
            price_max=100
        )
        search_event_name = 'tttest2'
        response = self.client.get(f'/api/events?event_name={search_event_name}', format='json')
        content_dict = self.content_to_dict(response.content)
        self.assertEqual(response.status_code, rest_status.HTTP_200_OK)
        self.assertEqual(len(content_dict), 1)

    def test_search_by_ticket_cost(self):
        EventFactory.create(
            event_name='tttest',
            start_datetime_at=datetime.datetime.now(),
            promoter_name='test_organizer_name',
            price_min=10.1,
            price_max=20
        )

        EventFactory.create(
            event_name='tttest2',
            start_datetime_at=datetime.datetime.now(),
            promoter_name='test_organizer_name',
            price_min=50,
            price_max=100
        )
        ticket_cost = 70
        response = self.client.get(f'/api/events?ticket_cost={ticket_cost}', format='json')
        content_dict = self.content_to_dict(response.content)
        self.assertEqual(response.status_code, rest_status.HTTP_200_OK)
        self.assertEqual(len(content_dict), 1)
        self.assertEqual(content_dict[0]['event_name'], 'tttest2')

    def test_ok_update(self):
        event = EventFactory.create(
            event_name='tttest',
            start_datetime_at=datetime.datetime.now(),
            promoter_name='test_organizer_name',
            price_min=10.1,
            price_max=100
        )

        data_in = {
            'event_name': 'test3',
            'promoter_name': 'test_name3'
        }

        response = self.client.put(f'/api/events/{event.id}', data_in, format='json')
        content_dict = self.content_to_dict(response.content)
        print(content_dict)
        self.assertEqual(response.status_code, rest_status.HTTP_200_OK)
        event = Event.objects.get()
        self.assertEqual(content_dict['event_name'], event.event_name)
        self.assertEqual(content_dict['promoter_name'], event.promoter_name)

    def test_john_validation(self):
        event = EventFactory.create(
            event_name='tttest',
            start_datetime_at=datetime.datetime.now(),
            promoter_name='test_organizer_name',
            price_min=10.1,
            price_max=100
        )

        data_in = {
            'event_name': 'test3',
            'promoter_name': 'john'
        }

        response = self.client.put(f'/api/events/{event.id}', data_in, format='json')
        content_dict = self.content_to_dict(response.content)
        print(content_dict)
        self.assertEqual(response.status_code, rest_status.HTTP_400_BAD_REQUEST)
