from django.urls import path
from .views import PopularSearchesView, UserViewHistoryView, RecordPropertyViewView

urlpatterns = [
    path('popular-searches/', PopularSearchesView.as_view(), name='popular-searches'),
    path('history/', UserViewHistoryView.as_view(), name='view-history'),
    path('record/<int:property_id>/', RecordPropertyViewView.as_view(), name='record-view'),


]