from app_event.models import Event
from common.serializers import CommonSerializer
from rest_framework import serializers


def john_validator(value):
    # john is not valid name :-)
    if value == 'john':
        raise serializers.ValidationError('john is not valid name')


class EventSearchQuerySerializer(CommonSerializer):
    event_name = serializers.CharField(required=False)
    start_datetime_at = serializers.DateTimeField(required=False)
    promoter_name = serializers.CharField(required=False)
    ticket_cost = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)


class EventSearchResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'event_name',
            'start_datetime_at',
            'promoter_name',
            'price_min',
            'price_max'
        )


class UpdateEventSerializer(serializers.ModelSerializer):
    promoter_name = serializers.CharField(validators=[john_validator])

    class Meta:
        model = Event
        fields = (
            'event_name',
            'promoter_name',
            # add more fields if you need
        )
