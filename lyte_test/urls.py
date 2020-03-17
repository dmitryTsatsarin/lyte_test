"""lyte_test URL Configuration """

from django.urls import path, include

urlpatterns = [
    path('api/', include('app_event.urls'))
]
