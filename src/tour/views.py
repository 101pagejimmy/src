from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from datetime import datetime
from django.conf import settings
from datetime import datetime, timezone
from django import forms
from schedule.views import Event

from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.utils import timezone
from django_filters import FilterSet, CharFilter, NumberFilter, DateFilter
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
import os
import string

import json
from schedule.models.events import Event, EventRelation

from .models import Guide
from .forms import GuideForm, GuideBookingForm, BookingFormSet, EventForm, OccurrenceForm

# Create your views here.

def landing(request):
	context = {}
	template = 'tour/landing_page.html'
	return render(request, template, context)



def home(request):
	guides = Guide.objects.all()[:6]
	context = {"guides": guides}
	template = 'home.html'
	return render(request, template, context)

#__________________________________________________________________


def create_tour_guide(request):
	form = GuideForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.guide_name = request.user
		instance.timestamp = timezone.now().date()
		instance.save()
		# message success
		# messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request, "tour/create_tour_guide.html", context)

#____________________________________________________________________


def guide_profile(request, calendar_slug=None):
	guide_profile = get_object_or_404(Guide, slug=slug)
	context = {"guide_profile": guide_profile,}
	template = "tour/guide_profile.html"
	return render(request, template, context)



def guide_profile_update(request, pk=None):

	guide_profile = get_object_or_404(Guide, pk=pk)
	form = GuideForm(request.POST or None, request.FILES or None, instance=guide_profile)
	if form.is_valid():

		guide_profile = form.save(commit=False)
		guide_profile.save()
		#messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(guide_profile.get_absolute_url())

	context = {
		"guide_profile": guide_profile,
		"form":form,
	}
	return render(request, "tour/create_tour_guide.html", context)

#____________________________________________________________


class GuideFilterTourDateForm(FilterSet):
	availiable = DateFilter(lookup_type='gte', label='Date from', name='start', widget=forms.TextInput(attrs={'class':'datepicker'}))
	
	class Meta:
		model = Event
		fields = ['start']


class GuideFilterForm(FilterSet):
	living = CharFilter(name='living', lookup_type='icontains', distinct=False)
	language = CharFilter(name='language', lookup_type='icontains', distinct=False)
	availiable = DateFilter(lookup_type='gte', name='events', distinct=False, widget=forms.TextInput(attrs={'class':'datepicker'}))
	
	class Meta:
		model = Guide
		fields = ['language', 'living', 'events']



class FilterMixin(object):
	filter_class = None
	search_ordering_param = "ordering"

	def get_queryset(self, *args, **kwargs):
		try:
			qs = super(FilterMixin, self).get_queryset(*args, **kwargs)
			return qs
		except:
			raise ImproperlyConfigured("You must have a queryset in order to use the FilterMixin")

	def get_context_data(self, *args, **kwargs):
		context = super(FilterMixin, self).get_context_data(*args, **kwargs)
		qs = self.get_queryset()
		ordering = self.request.GET.get(self.search_ordering_param)
		if ordering:
			qs = qs.order_by(ordering)
		filter_class = self.filter_class
		if filter_class:
			f = filter_class(self.request.GET, queryset=qs)
			context["object_list"] = f
		return context

#____________________________________________________________


class GuideListView(FilterMixin, ListView):
	model = Guide
	
	queryset = Guide.objects.all()
	filter_class = GuideFilterForm

	def get_context_data(self, *args, **kwargs):
		context = super(GuideListView, self).get_context_data(*args, **kwargs)
		context["now"] = timezone.now()
		context["query"] = self.request.GET.get("q") #None
		context["filter_form"] = GuideFilterForm(data=self.request.GET or None)

		queryset = Guide.objects.get_queryset()
		paginator = Paginator(queryset, 5)
		page = self.request.GET.get('page') 
		try: 
			document = paginator.page(page) 
		except PageNotAnInteger:
			document = paginator.page(1) 
		except EmptyPage:
			document = paginator.page(paginator.num_pages)
		context['document'] = document		

		return context

	
	def get_current_path(request):
		return {'current_path': request.get_full_path()}

	def get_queryset(self, *args, **kwargs):
		qs = super(GuideListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(language__icontains=query) |
				Q(living__icontains=query) |
				Q(events__gte=query)
				)
			print(query)
		return qs



#_____________________IN THE WORKS________________________________________________________

from schedule.models.events import Event, Occurrence
from schedule.models.calendars import Calendar
import datetime
import pytz
class GuideDetailView(DetailView):
	model = Guide

	def get_context_data(self, *args, **kwargs):
		context = super(GuideDetailView, self).get_context_data(*args, **kwargs)
		form = OccurrenceForm
		context["instance"] = self.get_object()
		context["current_user"] = self.request.user
		context['form'] = GuideBookingForm()
		context['guide_tours'] = OccurrenceForm(guide=self.get_object().pk)
		context['tours_dates'] = OccurrenceForm(guide=self.get_object().pk)

		
		#________CREATES OR GETS TOUR GUIDES CALANDER____________
		user = self.get_object().guide_name
		user_calendar = Calendar.objects.get_or_create_calendar_for_object(user, name = str(self.get_object().guide_name))
		context['calendar'] = user_calendar.get_absolute_url
		#________CREATES OR GETS TOUR GUIDES CALANDER____________

		#________GETS OCCURENCES FOR FOR THE USERS CALANDER____________
		#tours = Event.objects.filter(creator=self.get_object().pk)
		tours = EventRelation.objects.get_events_for_object(user)
		context['tours_list'] = EventRelation.objects.get_events_for_object(user)
		dates = self.request.get_full_path()
		tourlist = []
		for tour in tours:
			tourlist.append(tour.get_occurrences(\
				pytz.utc.localize(datetime.datetime(2016, 8, 15)),\
				pytz.utc.localize(datetime.datetime(2018, 8, 15, 8))\
				))
		context['tours'] = tourlist
		#________GETS OCCURENCES FOR FOR THE USERS CALANDER____________

		

		return context

	def get_current_path(request):
		return {'current_path': request.get_full_path()}


	def post(self, request, *args, **kwargs):
		self.status_form = GuideBookingForm(self.request.POST or None)
		if self.status_form.is_valid():
			request.POST = request.POST.copy()
			request.POST['tourSize'] = request.POST['tourSize']
			instance = self.get_object()
			try:
				instance.tourSize = instance.tourSize - int(request.POST['tourSize'])
				if instance.tourSize <= 0:
					print('NO MORE SPOTS!')
				else:
					instance.save()
			except:
				print('no more spots availiable for now')

		else:
			return super(GuideDetailView, self).post(request, *args, **kwargs)



#_____________________IN THE WORKS________________________________________________________


def create_post(request):

    if request.method == 'POST':
        book_tour = request.POST.get('post-text')
        response_data = {}

        post = Guide(tourSize=post_text)
        post.save()

        response_data['text'] = post.text

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )