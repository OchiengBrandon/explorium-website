from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'organization', 'is_teacher', 'is_student')
    list_filter = ('is_teacher', 'is_student')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'organization')