from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import UtilityType, Pipeline
from .serializers import UtilityTypeSerializer, PipelineSerializer
from users.permissions import IsEngineerOrAdmin

class UtilityTypeViewSet(viewsets.ModelViewSet):
    queryset = UtilityType.objects.all()
    serializer_class = UtilityTypeSerializer
    permission_classes = [IsEngineerOrAdmin]

class PipelineViewSet(viewsets.ModelViewSet):
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer
    permission_classes = [IsEngineerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['utility_type', 'city', 'condition']
    search_fields = ['name', 'owner']

    @action(detail=False, methods=['get'])
    def by_city(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response({'error': 'City parameter required'}, status=400)

        pipelines = self.queryset.filter(city=city)
        serializer = self.get_serializer(pipelines, many=True)
        return Response(serializer.data)