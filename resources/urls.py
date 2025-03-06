from django.urls import path
from .views import (
    ResourceListView, ResourceDetailView, resource_download,
    TeachingMaterialListView, TeachingMaterialDetailView, teaching_material_download
)

app_name = 'resources'  

urlpatterns = [
    path('', ResourceListView.as_view(), name='resource_list'),
    path('category/<slug:category_slug>/', ResourceListView.as_view(), name='resource_list_by_category'),
    path('<slug:slug>/', ResourceDetailView.as_view(), name='resource_detail'),
    path('<slug:slug>/download/', resource_download, name='resource_download'),
    path('teaching-materials/', TeachingMaterialListView.as_view(), name='teaching_material_list'),
    path('teaching-materials/<slug:slug>/', TeachingMaterialDetailView.as_view(), name='teaching_material_detail'),
    path('teaching-materials/<slug:slug>/download/', teaching_material_download, name='teaching_material_download'),
]