from django.utils import timezone
from rest_framework import serializers


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise serializers.ValidationError('Проверьте вводимый год!')
    return value
