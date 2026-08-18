from django.shortcuts import render
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
    
