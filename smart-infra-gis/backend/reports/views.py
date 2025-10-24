from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from projects.models import Project, Conflict
from gisdata.models import Pipeline
from django.db.models import Count, Q

class ReportStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        city = request.query_params.get('city')

        filters = {}
        if city:
            filters['city'] = city

        projects = Project.objects.filter(**filters)
        conflicts = Conflict.objects.filter(project__in=projects)
        pipelines = Pipeline.objects.filter(**filters)

        stats = {
            'total_projects': projects.count(),
            'total_conflicts': conflicts.count(),
            'resolved_conflicts': conflicts.filter(resolved=True).count(),
            'pending_conflicts': conflicts.filter(resolved=False).count(),
            'pipelines_count': pipelines.count(),
            'cost_savings': conflicts.count() * 50,  # ₹50L per conflict
            'critical_conflicts': conflicts.filter(severity='critical').count(),
            'high_conflicts': conflicts.filter(severity='high').count(),
            'medium_conflicts': conflicts.filter(severity='medium').count(),
            'low_conflicts': conflicts.filter(severity='low').count(),
        }

        return Response(stats)