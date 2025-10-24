from django.contrib.gis.geos import LineString, Point
from django.contrib.gis.measure import D
from gisdata.models import Pipeline
from .models import Conflict

def detect_conflicts(project):
    """
    Detect conflicts between a project and existing pipelines
    """
    conflicts = []

    if not project.geometry:
        return conflicts

    # Get pipelines in the same city
    pipelines = Pipeline.objects.filter(city=project.city)

    for pipeline in pipelines:
        # Check for direct overlap
        if project.geometry.intersects(pipeline.geometry):
            intersection = project.geometry.intersection(pipeline.geometry)

            if intersection.geom_type == 'Point':
                conflict_point = intersection
            elif intersection.geom_type == 'MultiPoint':
                conflict_point = intersection[0]
            else:
                conflict_point = Point(intersection.coords[0])

            conflict = Conflict.objects.create(
                project=project,
                pipeline=pipeline,
                conflict_type='overlap',
                severity='high',
                conflict_point=conflict_point,
                description=f"Project intersects with {pipeline.name}"
            )
            conflicts.append(conflict)

        # Check proximity (within 10 meters)
        else:
            distance = project.geometry.distance(pipeline.geometry) * 111000  # Convert to meters

            if distance < 10:
                # Find closest point
                closest_point = project.geometry.interpolate(
                    project.geometry.project(pipeline.geometry.centroid)
                )

                severity = 'medium' if distance < 5 else 'low'

                conflict = Conflict.objects.create(
                    project=project,
                    pipeline=pipeline,
                    conflict_type='proximity',
                    severity=severity,
                    distance=distance,
                    conflict_point=closest_point,
                    description=f"Project is {distance:.2f}m from {pipeline.name}"
                )
                conflicts.append(conflict)

    return conflicts