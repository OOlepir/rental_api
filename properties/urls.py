from django.urls import path
from .views import (
    PropertyListView, PropertyDetailView, PropertyTypeListView,
    LocationListView, PropertyCreateView, PropertyUpdateView,
    PropertyDeleteView, PropertyToggleStatusView
)

urlpatterns = [
    path('', PropertyListView.as_view(), name='property-list'),
    path('<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('create/', PropertyCreateView.as_view(), name='property-create'),
    path('<int:pk>/update/', PropertyUpdateView.as_view(), name='property-update'),
    path('<int:pk>/delete/', PropertyDeleteView.as_view(), name='property-delete'),
    path('<int:pk>/toggle-status/', PropertyToggleStatusView.as_view(), name='property-toggle-status'),
    path('types/', PropertyTypeListView.as_view(), name='property-types'),
    path('locations/', LocationListView.as_view(), name='locations'),
]