import json

from django.core.management.base import BaseCommand, CommandError

from moss.store.jwt import get_tokens_for_user
from moss.store.models import User


class Command(BaseCommand):
    """Create access and refresh tokens for a user"""

    def add_arguments(self, parser):
        parser.add_argument("user_id", type=int, help="The user id to get tokens for")

    def handle(self, *_args, **options):
        user = User.objects.get(id=options["user_id"])
        tokens = get_tokens_for_user(user)
        if self.stdout.isatty():
            self.stdout.write(self.style.SUCCESS("Generated tokens for user"))
            self.stdout.write(self.style.SUCCESS(f"Access: {tokens['access']}"))
            self.stdout.write(self.style.SUCCESS(f"Refresh: {tokens['refresh']}"))
        else:
            self.stdout.write(json.dumps(tokens))
