from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class City(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    region = models.CharField(max_length=255, blank=True)
    official_schedule_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "profiles_city"
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        
    def __str__(self):
        return f"{self.name} - ({self.region})"

class Place(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_places")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="places")
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=500, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        db_table = "profiles_place"
        verbose_name = _("Place")
        verbose_name_plural = _("Places")

    def __str__(self):
        return f"{self.title} - {self.city}"


class PlaceSubscription(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        ACTIVE = "active", _("Active")
        REJECTED = "rejected", _("Rejected")
        CANCELED = "canceled", _("Canceled")
        REMOVED = "removed", _("Removed")

    class Role(models.TextChoices):
        OWNER = "owner", _("Owner")
        SUBSCRIBER = "subscriber", _("Subscriber")

    place = models.ForeignKey(
        "Place",
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="place_subscriptions",
    )

    role = models.CharField(
        max_length=32,
        choices=Role.choices,
        default=Role.SUBSCRIBER,
    )
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.PENDING,
    )

    notifications_enabled = models.BooleanField(default=True)

    invited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sent_place_invites",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "profiles_place_subscription"
        verbose_name = _("Place Subscription")
        verbose_name_plural = _("Place Subscriptions")
        constraints = [
            models.UniqueConstraint(
                fields=["place", "user"],
                name="unique_place_user_subscription",
            )
        ]

    def __str__(self):
        return f"{self.user} -> {self.place} [{self.status}]"