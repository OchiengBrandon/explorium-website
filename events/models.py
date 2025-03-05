from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.utils import timezone

class EventCategory(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=120, unique=True)
    description = models.TextField(_("Description"), blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    
    class Meta:
        verbose_name = _("Event Category")
        verbose_name_plural = _("Event Categories")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Event(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=250, unique=True)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name='events')
    short_description = models.TextField(_("Short Description"))
    content = RichTextField(_("Content"))
    featured_image = models.ImageField(_("Featured Image"), upload_to='events/')
    location = models.CharField(_("Location"), max_length=200)
    address = models.TextField(_("Address"), blank=True)
    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(_("End Date"))
    registration_deadline = models.DateTimeField(_("Registration Deadline"), blank=True, null=True)
    capacity = models.PositiveIntegerField(_("Capacity"), default=0, help_text="0 means unlimited")
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2, default=0, help_text="0 means free")
    tags = TaggableManager(_("Tags"), blank=True)
    organizer = models.CharField(_("Organizer"), max_length=200, blank=True)
    organizer_website = models.URLField(_("Organizer Website"), blank=True)
    contact_email = models.EmailField(_("Contact Email"), blank=True)
    contact_phone = models.CharField(_("Contact Phone"), max_length=20, blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ['start_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def is_past(self):
        return self.end_date < timezone.now()
    
    @property
    def is_ongoing(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date
    
    @property
    def is_registration_open(self):
        if not self.registration_deadline:
            return not self.is_past
        return timezone.now() <= self.registration_deadline
    
    @property
    def available_seats(self):
        if self.capacity == 0:  # Unlimited
            return None
        registered = self.registrations.filter(status='confirmed').count()
        return max(0, self.capacity - registered)

class EventRegistration(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations', null=True, blank=True)
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=20, blank=True)
    organization = models.CharField(_("Organization"), max_length=200, blank=True)
    notes = models.TextField(_("Notes"), blank=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Event Registration")
        verbose_name_plural = _("Event Registrations")
        ordering = ['-created_at']
        unique_together = [['event', 'email']]
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"