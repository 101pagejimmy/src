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
        self.fields['event'].queryset = event

#________________________________IN THE WORKS______________________________________
    # def __init__(self, guide, *args, **kwargs):
    #     super(OccurrenceForm, self).__init__(*args, **kwargs)
    #     eventdic={}
    #     event = Event.objects.filter(creator = guide)
    #     for obj in event:
    #         obj.get_occurrences(pytz.utc.localize(datetime.datetime(2011, 8, 15, 8, 15, 12, 0)), pytz.utc.localize(datetime.datetime(2020, 8, 15, 8, 15, 12, 0)))
    #         for obj_1 in obj.get_occurrences(pytz.utc.localize(datetime.datetime(2011, 8, 15, 8, 15, 12, 0)), pytz.utc.localize(datetime.datetime(2020, 8, 15, 8, 15, 12, 0))):
    #             eventdic.setdefault(key,[]).append(obj_1.title)
#________________________________IN THE WORKS______________________________________
    class Meta:
        model = Occurrence
        fields = ['event']

# class NewEventForm(ModelForm):
#     class Meta:
#         model = 


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['start', 'end', 'title', 'creator']

class GuideForm(ModelForm):
    class Meta:
        model = Guide
        fields = ['first_name','last_name', 'tour_description', 'remember', 'language', 'living', 'tourSize']



class GuideBookingForm(ModelForm):
    class Meta:
        model = Guide

        fields = ['tourSize']
        widgets = {
            'tourSize': forms.TextInput(
                attrs={'id': 'post-text', 'required': True, 'placeholder': 'How many people?'}
            ),
        }

    

BookingFormSet = modelformset_factory(Guide, form=GuideBookingForm, extra=0)