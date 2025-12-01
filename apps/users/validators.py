# Django modules
from django.core.exceptions import ValidationError


_RESTRICTED_DOMAINS = {'spam.com', 'banned.com', 'fakeemail.com'}

def validate_email_domain(email: str) -> None:
    """
    Validate that the email domain is not in the restricted list.
    """
    domain: str = email.split('@')[-1]
    if domain in _RESTRICTED_DOMAINS:
        raise ValidationError(
            message=f"Email domain '{domain}' is not allowed.",
            code='invalid_domain'
        )

def validate_username_no_special_chars(username: str) -> None:
    """
    Validate that the username does not contain special characters.
    """
    if not username.isalnum():
        raise ValidationError(
            message="Username must be alphanumeric without special characters.",
            code='invalid_username'
        )