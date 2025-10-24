from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Project, Conflict

class ProjectSerializer(GeoFeatureModelSerializer):
    conflicts_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        geo_field = 'geometry'
        fields = ['id', 'name', 'project_type', 'description', 'department',
                  'city', 'start_date', 'end_date', 'estimated_cost', 'status',
                  'conflicts_count', 'created_at', 'updated_at']

    def get_conflicts_count(self, obj):
        return obj.conflicts.filter(resolved=False).count()

class ConflictSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    pipeline_name = serializers.CharField(source='pipeline.name', read_only=True)

    class Meta:
        model = Conflict
        fields = '__all__'