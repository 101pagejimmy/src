from rest_framework.serializers import ModelSerializer
from .models import Guide

class GuideSerializer(ModelSerializer):
    class Meta:
        model = Guide
        fields = ('guide_name', 'first_name', 'last_name', 'tourSize', 'language', 'tour_description', 'remember', \
         'living', 'secondary_language', 'meet_up_point', 'height_field', 'width_field', 'language', 'updated', 'timestamp', 'slug')
