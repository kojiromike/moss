"""Utility for making tokens available from the CLI"""

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """Get the access and refresh token for a user in a structured way."""
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
