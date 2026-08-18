from django.urls import path
from .views import SensorDataIngestionView

urlpatterns = [
    path('api/sensors/ingest/', SensorDataIngestionView.as_view(), name='sensor-ingest')
]

