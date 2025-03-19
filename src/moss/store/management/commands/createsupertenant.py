from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError, call_command

from moss.store.models import Tenant


class Command(createsuperuser.Command):
    """Create a tenant and superuser."""

    def handle(self, *_args, **_options):
        # Check if a default tenant exists, create one if not
        tenant, created = Tenant.objects.get_or_create(
            name="Aptible",
        )
        msg = (
            f"Created a tenant named {tenant.name} with the id of '{tenant.id}'"
            if created
            else f"A tenant named {tenant.name} exists with the id of '{tenant.id}'"
        )
        self.stdout.write(self.style.SUCCESS(msg))

        call_command("createsuperuser", tenant_id=tenant.id)
