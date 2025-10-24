from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import UtilityType, Pipeline

class UtilityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityType
        fields = '__all__'

class PipelineSerializer(GeoFeatureModelSerializer):
    utility_type_name = serializers.CharField(source='utility_type.name', read_only=True)

    class Meta:
        model = Pipeline
        geo_field = 'geometry'
        fields = ['id', 'name', 'utility_type', 'utility_type_name', 'diameter',
                  'depth', 'material', 'year_installed', 'condition', 'city',
                  'owner', 'created_at', 'updated_at']