from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from gisdata.models import Pipeline, UtilityType
import json

class Command(BaseCommand):
    help = 'Import GeoJSON data into Pipeline model'

    def add_arguments(self, parser):
        parser.add_argument('geojson_file', type=str, help='Path to GeoJSON file')
        parser.add_argument('--utility-type', type=str, required=True, help='Utility type name')
        parser.add_argument('--city', type=str, required=True, help='City name')

    def handle(self, *args, **options):
        geojson_file = options['geojson_file']
        utility_type_name = options['utility_type']
        city = options['city']

        # Get or create utility type
        utility_type, _ = UtilityType.objects.get_or_create(
            name=utility_type_name,
            defaults={'color': '#2196f3'}
        )

        # Load GeoJSON
        with open(geojson_file, 'r') as f:
            data = json.load(f)

        count = 0
        for feature in data['features']:
            properties = feature['properties']
            geometry = feature['geometry']

            Pipeline.objects.create(
                name=properties.get('name', f'Pipeline {count}'),
                utility_type=utility_type,
                geometry=json.dumps(geometry),
                diameter=properties.get('diameter', 100),
                depth=properties.get('depth', 1.5),
                material=properties.get('material', ''),
                year_installed=properties.get('year_installed'),
                city=city
            )
            count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported {count} pipelines')
        )