from django.contrib import admin
from .models import ProgramCategory, Program, ProgramImage, Curriculum

@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')
    search_fields = ('name', 'description')

class ProgramImageInline(admin.TabularInline):
    model = Program.gallery_images.through
    extra = 1

class CurriculumInline(admin.TabularInline):
    model = Curriculum
    extra = 1
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'audience', 'is_active', 'featured', 'created_at')
    list_filter = ('category', 'audience', 'is_active', 'featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description', 'content')
    inlines = [ProgramImageInline, CurriculumInline]
    filter_horizontal = ('gallery_images',)
    date_hierarchy = 'created_at'

@admin.register(ProgramImage)
class ProgramImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'caption', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'caption')

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'level', 'is_active', 'created_at')
    list_filter = ('level', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')