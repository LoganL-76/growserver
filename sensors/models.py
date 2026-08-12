from django.db import models
from grows.models import Plant

class Sensor(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='sensors', null=True, blank=True)
    sensor_type = models.CharField(max_length=50, choices=[
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
        ('light', 'Light'),
        ('pressure', 'Pressure'),
        ('soil1', 'Soil Moisture 1'),
        ('soil2', 'Soil Moisture 2'),
        ('soil3', 'Soil Moisture 3'),
        ('soil4', 'Soil Moisture 4'),
    ])
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.sensor_type} - {self.location}"
    
class SensorReading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sensor.sensor_type}: {self.value} at {self.timestamp}"
    