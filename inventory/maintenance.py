# inventory/maintenance.py

from datetime import datetime, timedelta
from .models import Software, SoftwareCatalog

def reconcile_licenses():
    now = datetime.utcnow()
    all_entries = Software.objects.filter(is_valid=True)

    for s in all_entries:
        metadata = SoftwareCatalog.objects.filter(name__icontains=s.software_name).first()
        if metadata and metadata.requires_license:
            if not s.license_key or (s.last_used_at and (now - s.last_used_at).days > metadata.reclaim_after_days):
                s.is_active_user = False  # Mark for reclaim
                s.save()
