from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class SiteSettings(models.Model):
    site_name = models.CharField(_("Site Name"), max_length=100, default="Explorium Organisation")
    site_description = models.TextField(_("Site Description"), blank=True)
    logo = models.ImageField(_("Logo"), upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(_("Favicon"), upload_to='site/', blank=True, null=True)
    email = models.EmailField(_("Contact Email"), blank=True)
    phone = models.CharField(_("Contact Phone"), max_length=20, blank=True)
    address = models.TextField(_("Address"), blank=True)
    facebook = models.URLField(_("Facebook URL"), blank=True)
    twitter = models.URLField(_("Twitter URL"), blank=True)
    instagram = models.URLField(_("Instagram URL"), blank=True)
    linkedin = models.URLField(_("LinkedIn URL"), blank=True)
    youtube = models.URLField(_("YouTube URL"), blank=True)
    
    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")
    
    def __str__(self):
        return self.site_name

class ContactMessage(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    subject = models.CharField(_("Subject"), max_length=200)
    message = models.TextField(_("Message"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    is_read = models.BooleanField(_("Is Read"), default=False)
    
    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class Testimonial(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    position = models.CharField(_("Position"), max_length=100, blank=True)
    image = models.ImageField(_("Image"), upload_to='testimonials/', blank=True, null=True)
    content = models.TextField(_("Content"))
    rating = models.PositiveSmallIntegerField(_("Rating"), default=5, choices=[(i, i) for i in range(1, 6)])
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    logo = models.ImageField(_("Logo"), upload_to='partners/')
    website = models.URLField(_("Website"), blank=True)
    description = models.TextField(_("Description"), blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    
    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")
        ordering = ['name']
    
    def __str__(self):
        return self.name

class TeamMember(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    position = models.CharField(_("Position"), max_length=100)
    image = models.ImageField(_("Image"), upload_to='team/')
    bio = RichTextField(_("Biography"))
    email = models.EmailField(_("Email"), blank=True)
    linkedin = models.URLField(_("LinkedIn"), blank=True)
    twitter = models.URLField(_("Twitter"), blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    order = models.PositiveSmallIntegerField(_("Order"), default=0)
    
    class Meta:
        verbose_name = _("Team Member")
        verbose_name_plural = _("Team Members")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = models.CharField(_("Question"), max_length=255)
    answer = RichTextField(_("Answer"))
    category = models.CharField(_("Category"), max_length=100, blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    order = models.PositiveSmallIntegerField(_("Order"), default=0)
    
    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ['order', 'question']
    
    def __str__(self):
        return self.question

class Newsletter(models.Model):
    email = models.EmailField(_("Email"), unique=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Newsletter Subscription")
        verbose_name_plural = _("Newsletter Subscriptions")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email