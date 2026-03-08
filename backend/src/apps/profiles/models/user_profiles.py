from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    primary_city = models.ForeignKey(
        to="City",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="primary_users",
    )
    
    class Meta:
        db_table = "profiles_userprofile"
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
    
    def __str__(self):
        return f"Profile of {self.user.username}"
