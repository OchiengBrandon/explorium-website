from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.http import FileResponse, Http404
from django.db.models import F

from .models import Resource, ResourceCategory, TeachingMaterial

class ResourceListView(ListView):
    model = Resource
    template_name = 'resources/resource_list.html'
    context_object_name = 'resources'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Resource.objects.filter(is_active=True)
        
        # Filter by category if provided
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by type if provided
        resource_type = self.request.GET.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
            
        # Filter by audience if provided
        audience = self.request.GET.get('audience')
        if audience:
            queryset = queryset.filter(audience=audience)
            
        # Search query
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q) | queryset.filter(description__icontains=q)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ResourceCategory.objects.filter(is_active=True)
        context['resource_types'] = dict(Resource.TYPE_CHOICES)
        context['audiences'] = dict(Resource.AUDIENCE_CHOICES)
        
        # Add active category if filtering by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['active_category'] = get_object_or_404(ResourceCategory, slug=category_slug)
            
        return context

class ResourceDetailView(DetailView):
    model = Resource
    template_name = 'resources/resource_detail.html'
    context_object_name = 'resource'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_resources'] = Resource.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        return context

def resource_download(request, slug):
    resource = get_object_or_404(Resource, slug=slug, is_active=True)
    
    if not resource.file:
        raise Http404("No file to download")
    
    # Increment download counter
    Resource.objects.filter(id=resource.id).update(download_count=F('download_count') + 1)
    
    # Return file
    try:
        return FileResponse(resource.file, as_attachment=True)
    except:
        raise Http404("File not found")

class TeachingMaterialListView(ListView):
    model = TeachingMaterial
    template_name = 'resources/teaching_material_list.html'
    context_object_name = 'materials'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = TeachingMaterial.objects.filter(is_active=True)
        
        # Filter by level if provided
        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(level=level)
            
        # Filter by subject if provided
        subject = self.request.GET.get('subject')
        if subject:
            queryset = queryset.filter(subject=subject)
            
        # Search query
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q) | queryset.filter(description__icontains=q)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['levels'] = dict(TeachingMaterial.LEVEL_CHOICES)
        context['subjects'] = TeachingMaterial.objects.values_list('subject', flat=True).distinct()
        return context

class TeachingMaterialDetailView(DetailView):
    model = TeachingMaterial
    template_name = 'resources/teaching_material_detail.html'
    context_object_name = 'material'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_materials'] = TeachingMaterial.objects.filter(
            level=self.object.level,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        return context

def teaching_material_download(request, slug):
    material = get_object_or_404(TeachingMaterial, slug=slug, is_active=True)
    
    # Increment download counter
    TeachingMaterial.objects.filter(id=material.id).update(download_count=F('download_count') + 1)
    
    # Return file
    try:
        return FileResponse(material.file, as_attachment=True)
    except:
        raise Http404("File not found")