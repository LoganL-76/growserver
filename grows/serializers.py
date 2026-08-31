from rest_framework import serializers
from .models import Grow, Plant, Harvest, Expense, JournalEntry

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'grow', 'name', 'strain']

class GrowSerializer(serializers.ModelSerializer):
    plants = PlantSerializer(many=True, read_only=True)

    class Meta:
        model = Grow
        fields = ['id', 'name', 'start_date', 'end_date', 'status', 'notes', 'plants']

class HarvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harvest
        fields = ['id', 'plant', 'date', 'wet_weight', 'dry_weight']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'grow', 'category', 'description', 'amount', 'date']

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'grow', 'timestamp', 'body', 'photo']