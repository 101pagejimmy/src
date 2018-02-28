from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django import forms
from schedule.views import Event

from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from django.utils import timezone
from django_filters import FilterSet, CharFilter, NumberFilter, DateFilter, DateTimeFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User
import googlemaps

from schedule.models.events import Event, EventRelation, Occurrence
from .serializers import GuideSerializer
from rest_framework import generics

from .models import Guide
from .forms import GuideForm, GuideBookingForm, OccurrenceForm, OccurrenceBookingForm
from dateutil.relativedelta import relativedelta

from io import StringIO
from calendar import monthrange

from schedule.models.calendars import Calendar
from django.utils.decorators import method_decorator
from itertools import chain

import os, string, json, datetime, pytz, csv, calendar


# Create your views here.


def home(request):
	guides = Guide.objects.all()[:6]
	context = {"guides": guides}
	template = 'home.html'
	return render(request, template, context)


def about(request):
	template = 'about.html'
	return render(request, template)

#__________________________________________________________________

@login_required
def create_tour_guide(request):

	
	form = GuideForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.guide_name = request.user
		instance.timestamp = timezone.now().date()
		user = request.user
		# get or create teh calender upon the person creating a tour.
		user_calendar = Calendar.objects.get_or_create_calendar_for_object(user, name=user)
		instance.save()

		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url)
	context = {
		"form": form,
		"OccurrenceForm": OccurrenceForm,
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
		return HttpResponseRedirect(guide_profile.get_absolute_url)

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
			#object_list = list(chain(f, occurrence_list))
			object_list = f
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
		context['city'] = self.request.GET.get('living')

		queryset = Guide.objects.get_queryset().first()

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
	queryset = Occurrence.objects.all().order_by('event')
	filter_class = OccurenceFilterForm

	def get_context_data(self, *args, **kwargs):
		context = super(OccurrenceListView, self).get_context_data(*args, **kwargs)
		context["query"] = self.request.GET.get("q") #None
		context["filter_form"] = OccurenceFilterForm(data=self.request.GET or None)
		queryset = Occurrence.objects.get_queryset()
		#print(queryset.distinct('guide'))
		context['from'] = self.request.GET.get('living')
		context["current_user"] = self.request.user

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
			qs = (qs | qs2)

		except:
			pass
		return qs


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


class GuideDetailView(DetailView):
	model = Guide

	def get_context_data(self, *args, **kwargs):
		context = super(GuideDetailView, self).get_context_data(*args, **kwargs)

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
				pytz.utc.localize(datetime.datetime(now.year, 12, 31,))\
				))
		context['tours'] = tourlist
		#________GETS OCCURENCES FOR FOR THE USERS CALANDER____________
		for tour in tourlist:
			for occurrence in tour:
				if occurrence.DoesNotExist:
					occurrence.guide = self.get_object()
					occurrence.save()
				else:
					pass

		form = OccurrenceForm
		context["instance"] = self.get_object()
		context["current_user"] = self.request.user
		context['form'] = GuideBookingForm()

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


def obj_dict(obj):
    return obj.__dict__

import itertools





def tour_map(request):
	import requests

	API_KEY =settings.GOOGLE_MAPS_API_KEY


	# Geocoding an address

	if request.GET.get('living'):
		address = request.GET.get('living')

		api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, API_KEY))
		api_response_dict = api_response.json()

		if api_response_dict['status'] == 'OK':
		    latitude = api_response_dict['results'][0]['geometry']['location']['lat']
		    longitude = api_response_dict['results'][0]['geometry']['location']['lng']

		latitude = latitude
		longitude = longitude
	else:
		latitude = 122.676556
		longitude = 45.5230645



	now = datetime.datetime.now()
	from django.core import serializers



	API_KEY =settings.GOOGLE_MAPS_API_KEY

	tours_list = []
	tour_locations = Event.objects.all()
	for tour in tour_locations:
		tours_list.append(tour.get_occurrences(pytz.utc.localize(datetime.datetime(now.year, now.month, now.day)), pytz.utc.localize(datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1]))))


	occurrence_list = []
	for tour in tours_list:
		for t in tour:
			t.save()
			occurrence_list.append(t)

	from django.core.serializers.json import DjangoJSONEncoder

	json_list = serializers.serialize('json', occurrence_list)



	from django.db import connection
	cursor = connection.cursor()

	import math
	distance_unit = 3959
	connection.connection.create_function('acos', 1, math.acos)
	connection.connection.create_function('cos', 1, math.cos)
	connection.connection.create_function('radians', 1, math.radians)
	connection.connection.create_function('sin', 1, math.sin)

	sql = """SELECT id, (3959 * acos( cos( radians(37) ) * cos( radians( latitude ) ) *
	cos( radians( longitude ) - radians(-122) ) + sin( radians(37) ) * sin( radians( latitude ) ) ) )
		AS distance FROM schedule_occurrence WHERE distance < 700
		ORDER BY distance LIMIT 0 , 20;"""
	cursor.execute(sql)

	ids = [row[0] for row in cursor.fetchall()]

	context = {
		"tour_locations": tour_locations,
		"API_KEY": API_KEY,
		"occurrence_list": occurrence_list,
		"json_list": json_list,
		"latitude": latitude,
		"longitude": longitude,
	}
	return render(request, "tour/tour_map.html", context)