from django.urls import path

from app_event.views import SearchApi, UpdateEventApi

urlpatterns = [
    path('events/<int:id>', UpdateEventApi.as_view()),
    path('events', SearchApi.as_view()),
]