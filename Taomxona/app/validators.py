from django.core.exceptions import ValidationError
from datetime import date

def validate_age(value):
    if value > date.today().year - 18:
        raise ValidationError("User must be at least 18 years old.")
