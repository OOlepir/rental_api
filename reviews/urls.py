from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, PropertyReviewsView

router = DefaultRouter()
router.register(r'', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('property/<int:property_id>/', PropertyReviewsView.as_view(), name='property-reviews'),
]