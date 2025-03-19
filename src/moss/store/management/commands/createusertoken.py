import json

from django.core.management.base import BaseCommand, CommandError
from rest_framework_simplejwt.tokens import RefreshToken

from moss.store.models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


class Command(BaseCommand):
    """Create access and refresh tokens for a user"""

    def add_arguments(self, parser):
        parser.add_arguments("user_id", type=int, help="The user id to get tokens for")

    def handle(self, *_args, **_options):
        user = User.get(options["user_id"])
        tokens = get_tokens_for_user(user)
        if self.stdout.isatty():
            self.stdout.write(self.style.SUCCESS("Generated tokens for user"))
            self.stdout.write(self.style.SUCCESS(f"Access: {tokens['access']}"))
            self.stdout.write(self.style.SUCCESS(f"Refresh: {tokens['refresh']}"))
        else:
            json.dumps(tokens)
