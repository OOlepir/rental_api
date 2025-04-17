from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property, PropertyType, Location
from .serializers import PropertySerializer, PropertyTypeSerializer, LocationSerializer
from .filters import PropertyFilter


class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.filter(status='active')
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'location__city', 'location__district']
    ordering_fields = ['price', 'created_at', 'views_count']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Логіка для аналітики: збільшуємо лічильник переглядів
        if self.request.user.is_authenticated:
            # Тут можна додати логіку для запису історії переглядів
            pass
        return queryset


class PropertyDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Збільшуємо лічильник переглядів
        instance.views_count += 1
        instance.save()
        # Записуємо історію переглядів, якщо користувач авторизований
        if self.request.user.is_authenticated:
            # Тут можна додати логіку для запису історії переглядів
            pass
        return super().retrieve(request, *args, **kwargs)


class PropertyCreateView(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PropertyUpdateView(generics.UpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Перевіряємо, чи користувач є власником оголошення
        instance = self.get_object()
        if instance.owner != self.request.user:
            return Response(
                {"detail": "Вы не можете редактировать это объявление"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()


class PropertyDeleteView(generics.DestroyAPIView):
    queryset = Property.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        # Перевіряємо, чи користувач є власником оголошення
        if instance.owner != self.request.user:
            return Response(
                {"detail": "Вы не можете удалить это объявление"},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()


class PropertyToggleStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)
            # Перевіряємо, чи користувач є власником оголошення
            if property_obj.owner != request.user:
                return Response(
                    {"detail": "Вы не можете изменить статус этого объявления"},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Переключаємо статус
            if property_obj.status == 'active':
                property_obj.status = 'inactive'
            else:
                property_obj.status = 'active'

            property_obj.save()
            return Response(
                {"status": property_obj.status},
                status=status.HTTP_200_OK
            )
        except Property.DoesNotExist:
            return Response(
                {"detail": "Объявление не найдено"},
                status=status.HTTP_404_NOT_FOUND
            )


class PropertyTypeListView(generics.ListAPIView):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    permission_classes = [permissions.AllowAny]


class LocationListView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['city', 'district']