from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UtilityType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#000000')
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Pipeline(models.Model):
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ]

    name = models.CharField(max_length=200)
    utility_type = models.ForeignKey(UtilityType, on_delete=models.CASCADE, related_name='pipelines')
    geometry = models.LineStringField(srid=4326)
    diameter = models.FloatField(help_text='Diameter in mm')
    depth = models.FloatField(help_text='Depth in meters')
    material = models.CharField(max_length=100, blank=True)
    year_installed = models.IntegerField(null=True, blank=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    city = models.CharField(max_length=100)
    owner = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pipelines_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.utility_type.name}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['city', 'utility_type']),
        ]