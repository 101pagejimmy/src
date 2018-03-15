from rest_framework import serializers

from schedule.models import Event, Occurrence


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ("created_on", "updated_on")


class OccurrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occurrence
        exclude = ("cancelled", "original_start", "original_end", "created_on", "updated_on")