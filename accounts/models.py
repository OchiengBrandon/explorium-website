from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(_("Profile Picture"), upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(_("Biography"), blank=True)
    phone = models.CharField(_("Phone Number"), max_length=20, blank=True)
    organization = models.CharField(_("Organization"), max_length=100, blank=True)
    position = models.CharField(_("Position"), max_length=100, blank=True)
    address = models.TextField(_("Address"), blank=True)
    is_teacher = models.BooleanField(_("Is Teacher"), default=False)
    is_student = models.BooleanField(_("Is Student"), default=False)
    
    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username