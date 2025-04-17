from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['tenant', 'created_at', 'updated_at']

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['property', 'check_in_date', 'check_out_date', 'guests_count', 'notes']

class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'guests_count', 'notes', 'status']
        read_only_fields = ['tenant', 'property', 'created_at', 'updated_at']
