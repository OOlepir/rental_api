from rest_framework import serializers
from .models import Property, PropertyType, Location, PropertyImage


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'city', 'district', 'address', 'postal_code', 'latitude', 'longitude']


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['id', 'name']


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'is_main', 'created_at']


class PropertySerializer(serializers.ModelSerializer):
    property_type = PropertyTypeSerializer(read_only=True)
    property_type_id = serializers.PrimaryKeyRelatedField(
        queryset=PropertyType.objects.all(), source='property_type', write_only=True
    )
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='location', write_only=True
    )
    images = PropertyImageSerializer(many=True, read_only=True)
    owner_name = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'owner', 'owner_name',
            'property_type', 'property_type_id', 'location', 'location_id',
            'price', 'rooms', 'area', 'status', 'created_at',
            'updated_at', 'views_count', 'images'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at', 'views_count']

    def get_owner_name(self, obj):
        return f"{obj.owner.first_name} {obj.owner.last_name}"

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)