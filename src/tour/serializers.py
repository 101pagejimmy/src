from rest_framework.serializers import ModelSerializer

# Use this to send the Guide
from .models import Guide

# Use This to send the event data via JSON to the API
from schedule.models.events import Event 

class GuideSerializer(ModelSerializer):
    class Meta:
        model = Guide
        fields = ('guide_name', 'first_name', 'last_name', 'language', 'tour_description', 'remember', 'living', 'secondary_language', 'meet_up_point', 'height_field', 'width_field', 'language', 'updated', 'timestamp', 'slug')