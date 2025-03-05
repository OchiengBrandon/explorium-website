from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone

from .models import Testimonial, Partner, TeamMember, FAQ
from .forms import ContactForm, NewsletterForm
from programs.models import Program
from events.models import Event
from blog.models import Post


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:6]
        context['partners'] = Partner.objects.filter(is_active=True)[:8]
        context['programs'] = Program.objects.filter(is_active=True, featured=True)[:3]
        
        # Update this line to filter based on start_date
        context['upcoming_events'] = Event.objects.filter(is_active=True, start_date__gte=timezone.now()).order_by('start_date')[:3]
        
        context['recent_posts'] = Post.objects.filter(status='published').order_by('-published_at')[:3]
        context['newsletter_form'] = NewsletterForm()
        return context
    
    def post(self, request, *args, **kwargs):
        if 'newsletter_submit' in request.POST:
            form = NewsletterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Thank you for subscribing to our newsletter!")
            else:
                messages.error(request, "This email is already subscribed or invalid.")
        return redirect('home')

class AboutView(TemplateView):
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.filter(is_active=True)
        context['partners'] = Partner.objects.filter(is_active=True)
        return context

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your message has been sent. We'll get back to you soon!")
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    template_name = 'contact_success.html'

class FAQView(ListView):
    model = FAQ
    template_name = 'faq.html'
    context_object_name = 'faqs'
    
    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = FAQ.objects.filter(is_active=True).values_list('category', flat=True).distinct()
        context['categories'] = [c for c in categories if c]
        return context

def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Thank you for subscribing!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'This email is already subscribed or invalid.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})