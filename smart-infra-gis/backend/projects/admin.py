from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Project, Conflict

@admin.register(Project)
class ProjectAdmin(GISModelAdmin):
    list_display = ['name', 'project_type', 'city', 'status', 'start_date', 'created_at']
    list_filter = ['project_type', 'status', 'city']
    search_fields = ['name', 'description', 'department']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Conflict)
class ConflictAdmin(admin.ModelAdmin):
    list_display = ['project', 'pipeline', 'conflict_type', 'severity', 'resolved', 'detected_at']
    list_filter = ['conflict_type', 'severity', 'resolved']
    search_fields = ['project__name', 'pipeline__name']
    readonly_fields = ['detected_at']