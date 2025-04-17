from rest_framework import serializers
from .models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    user_name = serializers.SerializerMethodField()
    property_title = serializers.StringRelatedField(source='property.title', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'property', 'user', 'user_details', 'user_name',
                  'property_title', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def validate(self, data):
        # Перевіряємо, що користувач не залишає відгук на власну нерухомість
        if data['property'].owner == self.context['request'].user:
            raise serializers.ValidationError("Вы не можете оставлять отзывы на собственное жилье")

        # Перевіряємо, що користувач орендував це житло
        user_bookings = self.context['request'].user.bookings.filter(
            property=data['property'],
            status='completed'
        )

        if not user_bookings.exists():
            raise serializers.ValidationError(
                "Вы можете оставлять отзывы только на жилье, которое вы арендовали и где бронирование завершено"
            )

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)