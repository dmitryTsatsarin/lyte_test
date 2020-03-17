from django.db import models


class TicketmasterScrapedRawData(models.Model):
    content = models.TextField()
    url = models.URLField()
    status_code = models.IntegerField() # it can be useful to repeat broken requests


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    start_datetime_at = models.DateTimeField()
    promoter_name = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    finish_datetime_at = models.DateTimeField(null=True)
    price_min = models.DecimalField(max_digits=8, decimal_places=2)
    price_max = models.DecimalField(max_digits=8, decimal_places=2)

