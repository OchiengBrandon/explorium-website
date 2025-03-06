from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile_view(request):
    # Get or create the user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)

    # Extract first name and last name for display if needed
    first_name = profile.user.first_name
    last_name = profile.user.last_name

    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile,
        'first_name': first_name,
        'last_name': last_name,
    })

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add user-specific data to dashboard context
        return context