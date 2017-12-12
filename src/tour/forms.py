from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory

from .models import Guide
from schedule.models.events import Event, Occurrence
import datetime
import pytz

class OccurrenceForm(ModelForm):

    def __init__(self, guide, *args, **kwargs):
        super(OccurrenceForm, self).__init__(*args, **kwargs)
        event = Event.objects.filter(creator = guide)
        #self.fields['event'].queryset = event

    # class Meta:
    #     model = Occurrence
    #     fields = ['event']

    class Meta:
        model = Event
        fields = ['reservation_spots']


class GuideForm(ModelForm):
    class Meta:
        model = Guide
        fields = ['first_name','last_name', 'tour_description', 'remember', 'language', 'living', 'tourSize']



class GuideBookingForm(ModelForm):
    class Meta:
        model = Guide

        fields = ['tourSize']
        widgets = {
            'tourSize': forms.NumberInput(
                attrs={'id': 'post-text', 'required': True, 'value': 1}
            ),
        }

#____________________IN THE WORKS FOR BOOKING_____________________________________

class OccurrenceBookingForm(ModelForm):
    class Meta:
        model = Occurrence

        fields = ['spots_free']
        widgets = {
            'spots_free': forms.NumberInput(
                attrs={'id': 'post-text-occurrence', 'required': True, 'placeholder':  'How many people?'}
            ),
        }

#____________________IN THE WORKS FOR BOOKING_____________________________________