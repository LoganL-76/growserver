from rest_framework import serializers
from .models import SensorReading, Sensor

class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = ['id', 'sensor', 'timestamp','value']
        