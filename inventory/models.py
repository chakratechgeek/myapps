from django.db import models

class Software(models.Model):
    hostname = models.CharField(max_length=255)
    software_name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    license_key = models.CharField(max_length=255, blank=True, null=True)
    is_valid = models.BooleanField(default=True)
    installed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hostname} - {self.software_name} {self.version}"

class SoftwareCatalog(models.Model):
    name = models.CharField(max_length=255)
    requires_license = models.BooleanField(default=False)
    is_metered = models.BooleanField(default=False)  # true = usage tracked
    reclaim_after_days = models.IntegerField(default=30)
