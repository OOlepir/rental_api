from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from .models import Review
from .serializers import ReviewSerializer


class ReviewPermission(permissions.BasePermission):
    """
    Дозволяє орендарям створювати та редагувати свої відгуки
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.user_type == 'tenant'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управління відгуками
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewPermission]

    def get_queryset(self):
        queryset = Review.objects.all()

        # Фільтрація за нерухомістю
        property_id = self.request.query_params.get('property_id')
        if property_id:
            queryset = queryset.filter(property__id=property_id)

        # Фільтрація за рейтингом
        min_rating = self.request.query_params.get('min_rating')
        if min_rating and min_rating.isdigit():
            queryset = queryset.filter(rating__gte=int(min_rating))

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PropertyReviewsView(generics.ListAPIView):
    """
    Отримання всіх відгуків для конкретної нерухомості
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        return Review.objects.filter(property_id=property_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        avg_rating = queryset.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'average_rating': round(avg_rating, 1),
            'results': serializer.data
        })