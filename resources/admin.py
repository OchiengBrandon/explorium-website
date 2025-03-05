from django.contrib import admin
from .models import ResourceCategory, Resource, TeachingMaterial

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')
    search_fields = ('name', 'description')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'resource_type', 'audience', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'resource_type', 'audience', 'is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
    readonly_fields = ('download_count', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'

@admin.register(TeachingMaterial)
class TeachingMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'subject', 'is_active', 'download_count', 'created_at')
    list_filter = ('level', 'subject', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description', 'subject')
    readonly_fields = ('download_count', 'created_at')
    date_hierarchy = 'created_at'