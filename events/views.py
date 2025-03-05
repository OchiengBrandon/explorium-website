from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .models import Event, EventCategory, EventRegistration
from .forms import EventRegistrationForm

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Event.objects.filter(is_active=True)
        
        # Filter by category if provided
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by time period
        period = self.request.GET.get('period', 'upcoming')
        now = timezone.now()
        
        if period == 'past':
            queryset = queryset.filter(end_date__lt=now)
        elif period == 'ongoing':
            queryset = queryset.filter(start_date__lte=now, end_date__gte=now)
        elif period == 'upcoming':
            queryset = queryset.filter(start_date__gt=now)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.filter(is_active=True)
        context['current_period'] = self.request.GET.get('period', 'upcoming')
        
        # Add active category if filtering by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['active_category'] = get_object_or_404(EventCategory, slug=category_slug)
            
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if user is already registered
        if self.request.user.is_authenticated:
            user_registration = EventRegistration.objects.filter(
                event=self.object,
                user=self.request.user
            ).first()
            context['user_registration'] = user_registration
        
        # Registration form
        context['registration_form'] = EventRegistrationForm()
        
        # Related events
        context['related_events'] = Event.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id).order_by('start_date')[:3]
        
        return context

class EventRegistrationView(CreateView):
    model = EventRegistration
    form_class = EventRegistrationForm
    template_name = 'events/event_registration.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Get the event
        self.event = get_object_or_404(Event, slug=self.kwargs['slug'])
        
        # Check if registration is still open
        if not self.event.is_registration_open:
            messages.error(request, "Registration for this event is closed.")
            return HttpResponseRedirect(reverse('event_detail', kwargs={'slug': self.event.slug}))
        
        # Check if event has capacity
        if self.event.capacity > 0 and self.event.available_seats == 0:
            messages.error(request, "This event is fully booked.")
            return HttpResponseRedirect(reverse('event_detail', kwargs={'slug': self.event.slug}))
        
        # Check if user is already registered
        if request.user.is_authenticated:
            existing_registration = EventRegistration.objects.filter(
                event=self.event,
                user=request.user
            ).first()
            
            if existing_registration:
                messages.info(request, "You are already registered for this event.")
                return HttpResponseRedirect(reverse('event_detail', kwargs={'slug': self.event.slug}))
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.event
        return context
    
    def form_valid(self, form):
        registration = form.save(commit=False)
        registration.event = self.event
        
        # Associate with user if logged in
        if self.request.user.is_authenticated:
            registration.user = self.request.user
        
        registration.save()
        messages.success(self.request, "Your registration has been submitted successfully!")
        return HttpResponseRedirect(reverse('event_detail', kwargs={'slug': self.event.slug}))