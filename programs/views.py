from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Program, ProgramCategory, Curriculum

class ProgramListView(ListView):
    model = Program
    template_name = 'programs/program_list.html'
    context_object_name = 'programs'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Program.objects.filter(is_active=True)
        
        # Filter by category if provided
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by audience if provided
        audience = self.request.GET.get('audience')
        if audience:
            queryset = queryset.filter(audience=audience)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProgramCategory.objects.filter(is_active=True)
        
        # Add active category if filtering by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['active_category'] = get_object_or_404(ProgramCategory, slug=category_slug)
            
        return context

class ProgramDetailView(DetailView):
    model = Program
    template_name = 'programs/program_detail.html'
    context_object_name = 'program'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_programs'] = Program.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:3]
        return context

class CurriculumListView(ListView):
    model = Curriculum
    template_name = 'programs/curriculum_list.html'
    context_object_name = 'curricula'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Curriculum.objects.filter(is_active=True)
        
        # Filter by level if provided
        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(level=level)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['levels'] = dict(Curriculum.LEVEL_CHOICES)
        return context

class CurriculumDetailView(DetailView):
    model = Curriculum
    template_name = 'programs/curriculum_detail.html'
    context_object_name = 'curriculum'