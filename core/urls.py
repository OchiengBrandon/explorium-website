from django.urls import path
from .views import (
    HomeView, AboutView, ContactView, ContactSuccessView,
    FAQView, TeamView, newsletter_subscribe
)

app_name = 'core'  

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('team/', TeamView.as_view(), name='team'),  # Add this line for the team view
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/success/', ContactSuccessView.as_view(), name='contact_success'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('newsletter/subscribe/', newsletter_subscribe, name='newsletter_subscribe'),
]