from django.db import models
from django.utils import timezone


class Software(models.Model):
    hostname = models.CharField(max_length=255)
    software_name = models.CharField(max_length=255)
    version = models.CharField(max_length=100, blank=True)
    license_key = models.CharField(max_length=255, blank=True, default="")  # ✅ Add default
    is_valid = models.BooleanField(default=True)

    installed_at = models.DateTimeField(null=True, blank=True, default=timezone.now)  # ✅ Add default
    last_used_at = models.DateTimeField(null=True, blank=True)
    is_active_user = models.BooleanField(default=True)  # ✅ Add default
    def __str__(self):
        return f"{self.hostname} - {self.software_name} {self.version}"

class SoftwareCatalog(models.Model):
    name = models.CharField(max_length=255)
    requires_license = models.BooleanField(default=False)
    is_metered = models.BooleanField(default=False)  # true = usage tracked
    reclaim_after_days = models.IntegerField(default=30)
