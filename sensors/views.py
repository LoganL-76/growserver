from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Sensor, SensorReading

class SensorDataIngestionView(APIView):
    def post(self, request):
        data = request.data

        sensor_types = ['temperature', 'humidity', 'pressure', 'light', 'soil1', 'soil2', 'soil3', 'soil4']

        for sensor_type in sensor_types:
            if sensor_type in data:
                sensor, created = Sensor.objects.get_or_create(sensor_type=sensor_type, 
                                                               defaults={'location': 'grow_tent'}
                                                               )
                SensorReading.objects.create(sensor = sensor, value = data[sensor_type])
        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
    
class LatestReadingsView(APIView):
    def get(self, request):
        sensor_types = [
            'temperature',
            'humidity',
            'pressure',
            'light',
            'soil1',
            'soil2',
            'soil3',
            'soil4'
        ]

        result = {}
        for sensor_type in sensor_types:
            try:
                sensor = Sensor.objects.get(sensor_type=sensor_type)
                latest = sensor.readings.latest('timestamp')
                result[sensor_type] = {
                    'value': latest.value,
                    'timestamp': latest.timestamp
                }
            except (Sensor.DoesNotExist, SensorReading.DoesNotExist):
                result[sensor_type] = None

        return Response(result)

class HistoricalReadingsView(APIView):
    def get(self, request):
        sensor_type = request.query_params.get('sensor')
        hours = int(request.query_params.get('hours', 24))

        if not sensor_type:
            return Response(
                {'error': 'sensor parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            sensor = Sensor.objects.get(sensor_type=sensor_type)
        except Sensor.DoesNotExist:
            return Response(
                {'error': f'Sensor {sensor_type} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        since = timezone.now() - timedelta(hours=hours)
        readings = sensor.readings.filter(
            timestamp__gte=since
        ).order_by('-timestamp')

        data = [
            {'value': r.value, 'timestamp': r.timestamp}
            for r in readings
        ]

        return Response({'sensor': sensor_type, 'readings': data})