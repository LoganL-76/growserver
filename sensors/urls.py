from django.urls import path
from .views import SensorDataIngestionView, LatestReadingsView, HistoricalReadingsView

urlpatterns = [
    path('api/sensors/ingest/', SensorDataIngestionView.as_view(), name='sensor-ingest'),
    path('api/sensors/latest/', LatestReadingsView.as_view(), name='sensor-latest'),
    path('api/sensors/history/', HistoricalReadingsView.as_view(), name='sensor-history'),
]

