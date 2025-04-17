from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Booking
from .permissions import OnlyOwnerChangeStatus
from .serializers import BookingSerializer, BookingCreateSerializer, BookingUpdateSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управління бронюваннями
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, OnlyOwnerChangeStatus]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'tenant':
            # Орендар бачить тільки свої бронювання
            return Booking.objects.filter(tenant=user)
        elif user.user_type == 'landlord':
            # Власник бачить бронювання своїх об'єктів
            return Booking.objects.filter(property__owner=user)
        return Booking.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return BookingUpdateSerializer
        return BookingSerializer

    def perform_create(self, serializer):
        # Перевіряємо, що користувач є орендарем
        if self.request.user.user_type != 'tenant':
            raise PermissionDenied("Только арендаторы могут создавать бронирования")

        # Перевіряємо, що користувач не бронює власну нерухомість
        property_id = self.request.data.get('property')
        property_obj = serializer.validated_data['property']
        if property_obj.owner == self.request.user:
            raise PermissionDenied("Нельзя бронировать собственное жилье")

        serializer.save(tenant=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='status', description='Фільтр по статусу бронювання', required=False, type=str)
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Отримати список бронювань з можливістю фільтрації по статусу
        """
        status_filter = request.query_params.get('status')
        queryset = self.get_queryset()

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Підтвердження бронювання власником
        """
        booking = self.get_object()

        # Перевіряємо, що користувач є власником нерухомості
        if booking.property.owner != request.user:
            return Response(
                {"detail": "Вы не можете подтвердить это бронирование"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Перевіряємо, що бронювання в статусі "очікує підтвердження"
        if booking.status != 'pending':
            return Response(
                {"detail": f"Бронирование не может быть подтверждено, текущий статус: {booking.get_status_display()}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'confirmed'
        booking.save()

        return Response({"status": "confirmed", "message": "Бронирование подтверждено"})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Відхилення бронювання власником
        """
        booking = self.get_object()

        # Перевіряємо, що користувач є власником нерухомості
        if booking.property.owner != request.user:
            return Response(
                {"detail": "Вы не можете отклонить это бронирование"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Перевіряємо, що бронювання в статусі "очікує підтвердження"
        if booking.status != 'pending':
            return Response(
                {"detail": f"Бронирование не может быть отклонено, текущий статус: {booking.get_status_display()}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'rejected'
        booking.save()

        return Response({"status": "rejected", "message": "Бронирование отклонено"})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Скасування бронювання орендарем
        """
        booking = self.get_object()

        # Перевіряємо, що користувач є орендарем
        if booking.tenant != request.user:
            return Response(
                {"detail": "Вы не можете отменить это бронирование"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Перевіряємо, що бронювання можна скасувати (статус pending або confirmed)
        if booking.status not in ['pending', 'confirmed']:
            return Response(
                {"detail": f"Бронирование не может быть отменено, текущий статус: {booking.get_status_display()}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Перевіряємо дату заїзду (можна додати логіку штрафів)
        # if booking.check_in_date <= timezone.now().date():
        #     return Response(
        #         {"detail": "Бронирование не может быть отменено, так как дата заезда уже наступила"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        booking.status = 'canceled'
        booking.save()

        return Response({"status": "canceled", "message": "Бронирование отменено"})