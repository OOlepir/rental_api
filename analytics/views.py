from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from .models import SearchHistory, ViewHistory
from .serializers import SearchHistorySerializer, ViewHistorySerializer, PopularSearchSerializer
from properties.models import Property


class PopularSearchesView(generics.ListAPIView):
    """
    Отримання популярних пошукових запитів
    """
    serializer_class = PopularSearchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Отримуємо статистику за останній місяць
        last_month = timezone.now() - timedelta(days=30)

        return SearchHistory.objects.filter(
            timestamp__gte=last_month
        ).values('query').annotate(
            count=Count('query')
        ).order_by('-count')[:10]


class UserViewHistoryView(generics.ListAPIView):
    """
    Отримання історії переглядів поточного користувача
    """
    serializer_class = ViewHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ViewHistory.objects.filter(
            user=self.request.user
        ).order_by('-timestamp')


class RecordPropertyViewView(APIView):
    """
    Запис перегляду нерухомості користувачем
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, property_id):
        try:
            property_obj = Property.objects.get(pk=property_id)

            # Створюємо або оновлюємо запис про перегляд
            view_history, created = ViewHistory.objects.get_or_create(
                user=request.user,
                property=property_obj,
                defaults={'timestamp': timezone.now()}
            )

            # Якщо запис вже існував, оновлюємо timestamp
            if not created:
                view_history.timestamp = timezone.now()
                view_history.save()

            # Збільшуємо лічильник переглядів
            property_obj.views_count += 1
            property_obj.save()

            return Response(
                {"message": "Просмотр объявления записан"},
                status=status.HTTP_200_OK
            )
        except Property.DoesNotExist:
            return Response(
                {"detail": "Объявление не найдено"},
                status=status.HTTP_404_NOT_FOUND
            )