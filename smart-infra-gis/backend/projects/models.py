from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    PROJECT_TYPES = [
        ('road', 'Road Construction'),
        ('metro', 'Metro Line'),
        ('pipeline', 'Pipeline Installation'),
        ('drainage', 'Drainage System'),
        ('building', 'Building Construction'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]

    name = models.CharField(max_length=300)
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPES)
    geometry = models.LineStringField(srid=4326, null=True, blank=True)
    polygon_area = models.PolygonField(srid=4326, null=True, blank=True)
    description = models.TextField(blank=True)
    department = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

    class Meta:
        ordering = ['-created_at']

class Conflict(models.Model):
    CONFLICT_TYPES = [
        ('overlap', 'Direct Overlap'),
        ('depth_clash', 'Depth Clash'),
        ('proximity', 'Too Close (<10m)'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='conflicts')
    pipeline = models.ForeignKey('gisdata.Pipeline', on_delete=models.CASCADE, related_name='conflicts')
    conflict_type = models.CharField(max_length=20, choices=CONFLICT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    distance = models.FloatField(help_text='Distance in meters', null=True, blank=True)
    conflict_point = models.PointField(srid=4326, null=True, blank=True)
    description = models.TextField(blank=True)
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - {self.conflict_type} with {self.pipeline.name}"

    class Meta:
        ordering = ['-severity', '-detected_at']