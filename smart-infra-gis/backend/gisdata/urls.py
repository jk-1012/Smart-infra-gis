from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UtilityTypeViewSet, PipelineViewSet

router = DefaultRouter()
router.register('utility-types', UtilityTypeViewSet)
router.register('pipelines', PipelineViewSet)

urlpatterns = [
    path('', include(router.urls)),
]