from rest_framework import serializers
from .models import SearchHistory, ViewHistory
from properties.serializers import PropertySerializer


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['id', 'user', 'query', 'timestamp']
        read_only_fields = ['user']


class ViewHistorySerializer(serializers.ModelSerializer):
    property_details = PropertySerializer(source='property', read_only=True)

    class Meta:
        model = ViewHistory
        fields = ['id', 'user', 'property', 'property_details', 'timestamp']
        read_only_fields = ['user']


class PopularSearchSerializer(serializers.Serializer):
    query = serializers.CharField()
    count = serializers.IntegerField()