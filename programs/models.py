from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

class ProgramCategory(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=120, unique=True)
    description = models.TextField(_("Description"), blank=True)
    icon = models.CharField(_("Icon Class"), max_length=50, blank=True, help_text="Font Awesome icon class")
    is_active = models.BooleanField(_("Is Active"), default=True)
    order = models.PositiveSmallIntegerField(_("Order"), default=0)
    
    class Meta:
        verbose_name = _("Program Category")
        verbose_name_plural = _("Program Categories")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Program(models.Model):
    AUDIENCE_CHOICES = (
        ('all', 'All Ages'),
        ('children', 'Children'),
        ('teenagers', 'Teenagers'),
        ('adults', 'Adults'),
        ('teachers', 'Teachers'),
        ('families', 'Families'),
    )
    
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=250, unique=True)
    category = models.ForeignKey(ProgramCategory, on_delete=models.CASCADE, related_name='programs')
    short_description = models.TextField(_("Short Description"))
    content = RichTextField(_("Content"))
    featured_image = models.ImageField(_("Featured Image"), upload_to='programs/')
    gallery_images = models.ManyToManyField('ProgramImage', blank=True, related_name='programs')
    audience = models.CharField(_("Target Audience"), max_length=20, choices=AUDIENCE_CHOICES, default='all')
    duration = models.CharField(_("Duration"), max_length=100, blank=True)
    location = models.CharField(_("Location"), max_length=200, blank=True)
    tags = TaggableManager(_("Tags"), blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    featured = models.BooleanField(_("Featured"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Program")
        verbose_name_plural = _("Programs")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ProgramImage(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    image = models.ImageField(_("Image"), upload_to='program_gallery/')
    caption = models.CharField(_("Caption"), max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(_("Order"), default=0)
    
    class Meta:
        verbose_name = _("Program Image")
        verbose_name_plural = _("Program Images")
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Curriculum(models.Model):
    LEVEL_CHOICES = (
        ('primary', 'Primary School'),
        ('secondary', 'Secondary School'),
        ('higher', 'Higher Education'),
        ('professional', 'Professional Development'),
    )
    
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=250, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='curricula')
    level = models.CharField(_("Education Level"), max_length=20, choices=LEVEL_CHOICES)
    description = RichTextField(_("Description"))
    file = models.FileField(_("Curriculum File"), upload_to='curricula/', blank=True, null=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Curriculum")
        verbose_name_plural = _("Curricula")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)