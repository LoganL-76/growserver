from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Grow, Plant, Harvest, Expense, JournalEntry
from .serializers import (
    GrowSerializer, PlantSerializer,
    HarvestSerializer, ExpenseSerializer, 
    JournalEntrySerializer
)


class GrowListView(APIView):
    def get(self, request):
        grows = Grow.objects.all().order_by('-start_date')
        serializer = GrowSerializer(grows, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GrowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GrowDetailView(APIView):
    def get_object(self, pk):
        try:
            return Grow.objects.get(pk=pk)
        except Grow.DoesNotExist:
            return None

    def get(self, request, pk):
        grow = self.get_object(pk)
        if not grow:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GrowSerializer(grow)
        return Response(serializer.data)

    def patch(self, request, pk):
        grow = self.get_object(pk)
        if not grow:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GrowSerializer(grow, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        grow = self.get_object(pk)
        if not grow:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        grow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PlantListView(APIView):
    def get(self, request):
        grow_id = request.query_params.get('grow')
        if grow_id:
            plants = Plant.objects.filter(grow=grow_id)
        else:
            plants = Plant.objects.all()
        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HarvestListView(APIView):
    def get(self, request):
        harvests = Harvest.objects.all().order_by('-date')
        serializer = HarvestSerializer(harvests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HarvestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpenseListView(APIView):
    def get(self, request):
        grow_id = request.query_params.get('grow')
        if grow_id:
            expenses = Expense.objects.filter(grow_id=grow_id).order_by('-date')
        else:
            expenses = Expense.objects.all().order_by('-date')
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JournalEntryListView(APIView):
    def get(self, request):
        grow_id = request.query_params.get('grow')
        if grow_id:
            entries = JournalEntry.objects.filter(grow_id=grow_id).order_by('-timestamp')
        else:
            entries = JournalEntry.objects.all().order_by('-timestamp')
        serializer = JournalEntrySerializer(entries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JournalEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
