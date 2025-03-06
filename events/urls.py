from django.urls import path
from .views import EventListView, EventDetailView, EventRegistrationView

app_name = 'events'  

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('category/<slug:category_slug>/', EventListView.as_view(), name='event_list_by_category'),
    path('<slug:slug>/', EventDetailView.as_view(), name='event_detail'),
    path('<slug:slug>/register/', EventRegistrationView.as_view(), name='event_registration'),
]