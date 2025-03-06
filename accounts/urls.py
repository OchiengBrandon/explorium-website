from django.urls import path
from .views import profile_view, DashboardView

app_name = 'accounts'  

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]