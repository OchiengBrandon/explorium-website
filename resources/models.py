from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

class ResourceCategory(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=120, unique=True)
    description = models.TextField(_("Description"), blank=True)
    icon = models.CharField(_("Icon Class"), max_length=50, blank=True, help_text="Font Awesome icon class")
    is_active = models.BooleanField(_("Is Active"), default=True)
    order = models.PositiveSmallIntegerField(_("Order"), default=0)
    
    class Meta:
        verbose_name = _("Resource Category")
        verbose_name_plural = _("Resource Categories")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Resource(models.Model):
    AUDIENCE_CHOICES = (
        ('all', 'All Ages'),
        ('children', 'Children'),
        ('teenagers', 'Teenagers'),
        ('adults', 'Adults'),
        ('teachers', 'Teachers'),
        ('parents', 'Parents'),
    )
    
    TYPE_CHOICES = (
        ('document', 'Document'),
        ('video', 'Video'),
        ('link', 'External Link'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('interactive', 'Interactive Content'),
    )
    
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=250, unique=True)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name='resources')
    resource_type = models.CharField(_("Resource Type"), max_length=20, choices=TYPE_CHOICES)
    audience = models.CharField(_("Target Audience"), max_length=20, choices=AUDIENCE_CHOICES, default='all')
    description = RichTextField(_("Description"))
    thumbnail = models.ImageField(_("Thumbnail"), upload_to='resources/thumbnails/', blank=True, null=True)
    file = models.FileField(_("File"), upload_to='resources/files/', blank=True, null=True)
    video_url = models.URLField(_("Video URL"), blank=True, help_text="YouTube or Vimeo URL")
    external_url = models.URLField(_("External URL"), blank=True)
    is_featured = models.BooleanField(_("Is Featured"), default=False)
    is_active = models.BooleanField(_("Is Active"), default=True)
    download_count = models.PositiveIntegerField(_("Download Count"), default=0)
    tags = TaggableManager(_("Tags"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Resource")
        verbose_name_plural = _("Resources")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class TeachingMaterial(models.Model):
    LEVEL_CHOICES = (
        ('primary', 'Primary School'),
        ('secondary', 'Secondary School'),
        ('higher', 'Higher Education'),
    )
    
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=250, unique=True)
    level = models.CharField(_("Education Level"), max_length=20, choices=LEVEL_CHOICES)
    subject = models.CharField(_("Subject"), max_length=100)
    description = RichTextField(_("Description"))
    file = models.FileField(_("File"), upload_to='teaching_materials/')
    thumbnail = models.ImageField(_("Thumbnail"), upload_to='teaching_materials/thumbnails/', blank=True, null=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    download_count = models.PositiveIntegerField(_("Download Count"), default=0)
    tags = TaggableManager(_("Tags"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Teaching Material")
        verbose_name_plural = _("Teaching Materials")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)