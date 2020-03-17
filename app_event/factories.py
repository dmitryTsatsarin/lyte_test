import factory

from app_event.models import Event


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event
