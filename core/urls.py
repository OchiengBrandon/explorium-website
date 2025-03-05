from django.urls import path
from .views import (
    HomeView, AboutView, ContactView, ContactSuccessView,
    FAQView, newsletter_subscribe
)

app_name = 'core'  # Set the namespace for this app

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/success/', ContactSuccessView.as_view(), name='contact_success'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('newsletter/subscribe/', newsletter_subscribe, name='newsletter_subscribe'),
]