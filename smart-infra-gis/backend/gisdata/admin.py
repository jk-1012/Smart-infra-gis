from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import UtilityType, Pipeline

@admin.register(UtilityType)
class UtilityTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'icon']
    search_fields = ['name']

@admin.register(Pipeline)
class PipelineAdmin(GISModelAdmin):
    list_display = ['name', 'utility_type', 'city', 'diameter', 'depth', 'condition', 'created_at']
    list_filter = ['utility_type', 'city', 'condition']
    search_fields = ['name', 'owner']
    readonly_fields = ['created_at', 'updated_at']