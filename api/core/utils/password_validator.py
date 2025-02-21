import re
from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    """
    Custom validator to enforce password policies:
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    - Minimum length of 8 characters
    """

    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("must be at least 8 characters long.")

        if not re.search(r"[A-Z]", password):
            raise ValidationError("must contain at least one uppercase letter.")

        if not re.search(r"[a-z]", password):
            raise ValidationError("must contain at least one lowercase letter.")

        if not re.search(r"\d", password):
            raise ValidationError("must contain at least one digit (0-9).")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("must contain at least one special character (!@#$%^&*(),.).")

    def get_help_text(self):
        return "must contain at least one uppercase letter, one lowercase letter, one digit, one special character, and be at least 8 characters long."
