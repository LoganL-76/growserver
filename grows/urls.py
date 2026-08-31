from django.urls import path
from .views import (
    GrowListView, GrowDetailView,
    PlantListView, HarvestListView,
    ExpenseListView, JournalEntryListView
)

urlpatterns = [
    path('api/grows/', GrowListView.as_view(), name='grow-list'),
    path('api/grows/<int:pk>/', GrowDetailView.as_view(), name='grow-detail'),
    path('api/plants/', PlantListView.as_view(), name='plant-list'),
    path('api/harvests/', HarvestListView.as_view(), name='harvest-list'),
    path('api/expenses/', ExpenseListView.as_view(), name='expense-list'),
    path('api/journal/', JournalEntryListView.as_view(), name='journal-list'),
]
