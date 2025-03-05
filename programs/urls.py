from django.urls import path
from .views import (
    ProgramListView, ProgramDetailView,
    CurriculumListView, CurriculumDetailView
)

app_name = 'programs'  # Set the namespace for this app

urlpatterns = [
    path('', ProgramListView.as_view(), name='program_list'),
    path('category/<slug:category_slug>/', ProgramListView.as_view(), name='program_list_by_category'),
    path('<slug:slug>/', ProgramDetailView.as_view(), name='program_detail'),
    path('curricula/', CurriculumListView.as_view(), name='curriculum_list'),
    path('curricula/<slug:slug>/', CurriculumDetailView.as_view(), name='curriculum_detail'),
]