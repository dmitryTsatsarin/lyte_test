from django.db.models import Q

from app_event.models import Event
from app_event.serializers import EventSearchQuerySerializer, EventSearchResponseSerializer, UpdateEventSerializer
from common.views import CommonGenericView


class SearchApi(CommonGenericView):
    serializer_class_query = EventSearchQuerySerializer
    serializer_class = EventSearchResponseSerializer

    def get_queryset(self):
        params_data = self.query_params_data

        ticket_cost = params_data.pop('ticket_cost', None)
        if ticket_cost:
            price_q = Q(price_min__lte=ticket_cost, price_max__gte=ticket_cost)
        else:
            price_q = Q()
        return Event.objects.filter(price_q,**params_data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UpdateEventApi(CommonGenericView):
    serializer_class = UpdateEventSerializer

    def custom_permission_validation(self):
        # add code here if you need
        pass


    def get_queryset(self):

        # add additional filtration if you need
        return Event.objects.filter()

    def put(self, request, *args, **kwargs):
        self.custom_permission_validation()
        return self.update(request, *args, **kwargs)
