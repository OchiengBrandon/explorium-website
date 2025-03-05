from django.contrib import admin
from .models import EventCategory, Event, EventRegistration

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_date', 'end_date', 'location', 'is_active', 'is_past')
    list_filter = ('category', 'is_active', 'start_date')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description', 'content', 'location')
    inlines = [EventRegistrationInline]
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at')
    
    def is_past(self, obj):
        return obj.is_past
    is_past.boolean = True
    is_past.short_description = "Past Event"

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event', 'status', 'created_at')
    list_filter = ('status', 'event')
    search_fields = ('name', 'email', 'phone', 'organization', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'