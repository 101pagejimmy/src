from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.conf import settings
from datetime import datetime, timezone
from django import forms
from schedule.views import Event
import datetime

from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from django.utils import timezone
from django_filters import FilterSet, CharFilter, NumberFilter, DateFilter, DateTimeFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User
import os
import string

import json
from schedule.models.events import Event, EventRelation, Occurrence
from .serializers import GuideSerializer
from rest_framework import generics

from .models import Guide
from .forms import GuideForm, GuideBookingForm, OccurrenceForm, OccurrenceBookingForm


from dateutil.relativedelta import relativedelta

from io import StringIO
import csv


from schedule.models.calendars import Calendar
import pytz

from itertools import chain

# Create your views here.


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


class GuideFilterForm(FilterSet):
	living = CharFilter(name='living', lookup_type='icontains', distinct=False)
	language = CharFilter(name='language', lookup_type='icontains', distinct=False)

	
	class Meta:
		model = Guide
		fields = ['language', 'living']




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

			#____________________IN THE WORKS FOR QUERYING_______
			date = self.request.GET['start']
			date_dash = date.replace('/', '-')
			occurrence_list = Occurrence.objects.filter(start__icontains=date_dash[:5])
			#occurrence_list = Occurrence.objects.filter(event__creator__exact='talia')
			object_list = list(chain(f, occurrence_list))
			#____________________IN THE WORKS FOR QUERYING_______
			context["object_list"] = object_list
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
		
        #______________________IN THE WORKS FOR PAGINATION__________________
		paginator = Paginator(queryset, 5)
		page = self.request.GET.get('page') 
		try: 
			document = paginator.page(page) 
		except PageNotAnInteger:
			document = paginator.page(1) 
		except EmptyPage:
			document = paginator.page(paginator.num_pages)
		context['document'] = document		
        #______________________IN THE WORKS FOR PAGINATION__________________


		return context

	
	def get_current_path(request):
		return {'current_path': request.get_full_path()}

	def get_queryset(self, *args, **kwargs):
		qs = super(GuideListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(language__icontains=query) |
				Q(living__icontains=query)
				)
		return qs



class OccurenceFilterForm(FilterSet):
	start = DateFilter(lookup_type='icontains', name='start', distinct=False)
	living = CharFilter(lookup_type='icontains', name='guide__living', distinct=False)
	language = CharFilter(lookup_type='icontains', name='guide__language', distinct=False)
	
	class Meta:
		model = Occurrence
		fields = ['start', 'guide']

class OccurenceFilterMixin(object):
	filter_class = None
	search_ordering_param = "ordering"

	def get_queryset(self, *args, **kwargs):
		try:
			qs = super(OccurenceFilterMixin, self).get_queryset(*args, **kwargs)
			return qs

		except:
			raise ImproperlyConfigured("You must have a queryset in order to use the OccurenceFilterMixin")

	def get_context_data(self, *args, **kwargs):
		context = super(OccurenceFilterMixin, self).get_context_data(*args, **kwargs)
		qs = self.get_queryset()
		ordering = self.request.GET.get(self.search_ordering_param)
		if ordering:
			qs = qs.order_by(ordering)
		filter_class = self.filter_class
		if filter_class:
			f = filter_class(self.request.GET, queryset=qs)
			context["object_list"] = f
		return context


class OccurrenceListView(OccurenceFilterMixin, ListView):
	model = Occurrence
	queryset = Occurrence.objects.all()
	filter_class = OccurenceFilterForm

	def get_context_data(self, *args, **kwargs):
		context = super(OccurrenceListView, self).get_context_data(*args, **kwargs)
		context["query"] = self.request.GET.get("q") #None
		context["filter_form"] = OccurenceFilterForm(data=self.request.GET or None)
		queryset = Occurrence.objects.get_queryset()
		
		return context


	def get_queryset(self, *args, **kwargs):
		qs = super(OccurrenceListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(start__icontains=query))
		try:		
			qs2 = self.model.objects.filter(
			Q(language=query) |
			Q(living=query)
				)
			qs = (qs | qs2).distinct()
		except:
			pass
		return qs


#_______________________IN THE WORKS FOR EMAIL BOOKING________________


def booking_email(user_name, user_email, bookings):
	title = 'Contact Us'
	title_align_center = True

	#user_email = request.user.email
	user_name = user_name
	subject = 'Free Walking Tour Guide Booking'
	form_message = 'You have booked %s spot/s for this date from this time to that time. Please show up at least 30 minutes early to this place' %(bookings)
	from_email = settings.EMAIL_HOST_USER
	total_bookings = bookings
	to_email = [from_email, 'hardiet@oregonstate.edu']
	contact_message = "%s: %s via %s"%( 
			user_name,
			total_bookings, 
			from_email)
	some_html_message = str(form_message)
		

		

	try:
		send_mail(subject, 
		contact_message, 
		from_email, 
		to_email, 
		html_message=some_html_message,
		fail_silently=True)
		return HttpResponseRedirect('/')
	except BadHeaderError:
		return HttpResponse('Invalid header found.')

	context = {
		"form": form,
		"title": title,
		"title_align_center": title_align_center,
	}

	return render(request, "forms.html", context)


#_______________________IN THE WORKS FOR EMAIL BOOKING________________




#_____________________IN THE WORKS________________________________________________________


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
		context['other_form'] = OccurrenceBookingForm()

		
		#________CREATES OR GETS TOUR GUIDES CALANDER____________
		user = self.get_object().guide_name
		user_calendar = Calendar.objects.get_or_create_calendar_for_object(user, name = str(self.get_object().guide_name))
		context['calendar'] = user_calendar.get_absolute_url
		#________CREATES OR GETS TOUR GUIDES CALANDER____________


		#________GETS OCCURENCES FOR FOR THE USERS CALANDER____________
		tours = EventRelation.objects.get_events_for_object(user)
		context['tours_list'] = EventRelation.objects.get_events_for_object(user)
		now = datetime.datetime.now()
		try:
			dates = self.request.POST.get['living']
		except:
			pass
		tourlist = []
		for tour in tours:
			tourlist.append(tour.get_occurrences(\
				pytz.utc.localize(datetime.datetime(now.year, now.month, now.day)),\
				#datetime.datetime(2013, 1, 5, 9, 0, tzinfo=pytz.utc),
				pytz.utc.localize(datetime.datetime(now.year, 8, 15,))\
				))
		context['tours'] = tourlist
		#________GETS OCCURENCES FOR FOR THE USERS CALANDER____________
		for tour in tourlist:
			for occurrence in tour:
				if occurrence.DoesNotExist:
					occurrence.save()
				else:
					pass


		
		return context

	def get_current_path(request):
		return {'current_path': request.get_full_path()}


	def post(self, request, *args, **kwargs):
		user = self.get_object().guide_name
		self.status_form = GuideBookingForm(self.request.POST or None)
		if self.status_form.is_valid():
			request.POST = request.POST.copy()
			spots_free = int(request.POST['spots_free'])
			tour_choosen = request.POST['tour']

			occurrence_list = []

			f = StringIO(tour_choosen)
			reader = csv.reader(f, delimiter=',')
			for row in reader:
				occurrence_list.append(row)

			year = int(occurrence_list[0][0])
			month = int(occurrence_list[0][1])
			day = int(occurrence_list[0][2])
			hour = int(occurrence_list[0][3])
			minute = int(occurrence_list[0][4])
			second = int(occurrence_list[0][5])


			booking_email(request.user, request.user.email, spots_free)


			tours = EventRelation.objects.get_events_for_object(user)
			for tour in tours:
				tour_occurrence = tour.get_occurrence(pytz.utc.localize(datetime.datetime(year, month, day, hour, minute, second)))
				tour_occurrence.spots_free -= spots_free
				tour_occurrence.save()
				return HttpResponseRedirect('/1')

		else:
			return super(GuideDetailView, self).post(request, *args, **kwargs)




#_______IN THE WORKS FOR REST_FRAMEWORK___________________
class GuideDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
#_______IN THE WORKS FOR REST_FRAMEWORK___________________