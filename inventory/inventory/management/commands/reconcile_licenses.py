from django.core.management.base import BaseCommand
from inventory.models import Software, SoftwareCatalog
from datetime import datetime

class Command(BaseCommand):
    help = 'Reconcile software licenses and flag inactive users'

    def handle(self, *args, **options):
        now = datetime.utcnow()
        updated_count = 0

        entries = Software.objects.filter(is_valid=True)

        for s in entries:
            catalog = SoftwareCatalog.objects.filter(name__icontains=s.software_name).first()
            if catalog and catalog.requires_license:
                if not s.license_key or (s.last_used_at and (now - s.last_used_at).days > catalog.reclaim_after_days):
                    s.is_active_user = False
                    s.save()
                    updated_count += 1

        self.stdout.write(self.style.SUCCESS(f"✔ Reconciled {updated_count} software records."))
