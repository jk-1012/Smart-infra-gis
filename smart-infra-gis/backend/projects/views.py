from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, Conflict
from .serializers import ProjectSerializer, ConflictSerializer
from .gis_conflict import detect_conflicts
from users.permissions import IsEngineerOrAdmin

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsEngineerOrAdmin]

    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        # Run conflict detection
        detect_conflicts(project)

    @action(detail=True, methods=['post'])
    def check_conflicts(self, request, pk=None):
        project = self.get_object()
        conflicts = detect_conflicts(project)
        serializer = ConflictSerializer(conflicts, many=True)
        return Response({
            'conflicts_found': len(conflicts),
            'conflicts': serializer.data
        })

    @action(detail=False, methods=['get'])
    def by_city(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response({'error': 'City parameter required'}, status=400)

        projects = self.queryset.filter(city=city)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

class ConflictViewSet(viewsets.ModelViewSet):
    queryset = Conflict.objects.all()
    serializer_class = ConflictSerializer
    permission_classes = [IsEngineerOrAdmin]

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        conflict = self.get_object()
        conflict.resolved = True
        conflict.resolution_notes = request.data.get('notes', '')
        conflict.save()
        return Response({'status': 'Conflict resolved'})