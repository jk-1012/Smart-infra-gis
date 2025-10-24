from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ConflictViewSet

router = DefaultRouter()
router.register('', ProjectViewSet)
router.register('conflicts', ConflictViewSet)

urlpatterns = [
    path('', include(router.urls)),
]