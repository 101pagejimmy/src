import decimal
import datetime
import pytz
import csv
import calendar
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from io import StringIO

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .forms import GuideForm, GuideBookingForm, OccurrenceForm
from .models import Guide
from django_filters import FilterSet, CharFilter, DateFilter
from schedule.models.calendars import Calendar
from schedule.models.events import Event, EventRelation, Occurrence
from schedule.views import get_occurrence

# Create your views here.


def home(request):
    guides = Guide.objects.all()[:6]
    context = {"guides": guides}
    template = 'home.html'
    return render(request, template, context)


def about(request):
    template = 'about.html'
    return render(request, template)


@login_required
def create_tour_guide(request):

    now = datetime.datetime.now()

    if request.is_ajax():
        event_id = request.GET.get('event-id')
        this_date = (request.GET.get('query-date')).split('-')
        year = int(this_date[0])
        month = int(this_date[1])
        day = int(this_date[2])
        event = Event.objects.get(id=event_id)
        tours_list = []
        tours_list.append([event.get_occurrences(pytz.utc.localize(datetime.datetime(year, month, day)),
                                                 pytz.utc.localize(datetime.datetime(now.year, now.month,
                                                                                     calendar.monthrange(now.year,
                                                                                                         now.month)[1])))])
        json_list = serializers.serialize('json', tours_list[0][0])
        data = {"json_list": json_list}
        return JsonResponse(data)

    form = GuideForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.guide_name = request.user
        instance.timestamp = timezone.now().date()
        user = request.user
        # get or create the calender upon a person becoming a tour guide.
        Calendar.objects.get_or_create_calendar_for_object(user, name=user)
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url)
    context = {
        "form": form,
        "OccurrenceForm": OccurrenceForm,
    }
    return render(request, "tour/create_tour_guide.html", context)


def tour_booker(request):
    if request.is_ajax():
        event_id = request.GET.get('eventID')
        booking_date = decimal.Decimal(request.GET.get('bookingDate'))
        hour = int(request.GET.get('hour'))
        tour_date = datetime.datetime.fromtimestamp(float(booking_date)/1000.0)
        date = pytz.utc.localize(datetime.datetime(tour_date.year, tour_date.month,
                                                   tour_date.day, hour, tour_date.minute,
                                                   tour_date.second))
        try:
            new_occ = Occurrence.objects.get(event=event_id, start=date)
            data = {"url": new_occ.get_absolute_url()}
            return JsonResponse(data)
        except:
            event, occurrence = get_occurrence(event_id, year=tour_date.year, month=tour_date.month,
                                               day=tour_date.day, hour=hour, minute=tour_date.minute,
                                               second=tour_date.second, tzinfo=pytz.utc)
            occurrence.save()
            data = {"url": occurrence.get_absolute_url()}
            return JsonResponse(data)


def calendar_event_creator(request):
    if request.is_ajax():
        new_date = request.GET.get('newDate')
        new_date_array = new_date.split("/")
        event_id = int(new_date_array[3])
        year = int(new_date_array[4])
        month = int(new_date_array[5])
        day = int(new_date_array[6])
        hour = int(new_date_array[7])
        minute = int(new_date_array[8])
        second = int(new_date_array[9])

        date = pytz.utc.localize(datetime.datetime(year, month, day, hour, minute, second))
        try:
            new_occ = Occurrence.objects.get(event=event_id, start=date)
            data = {"url": new_occ.get_absolute_url()}
            print(new_occ)
            return JsonResponse(data)
        except:
            event, occurrence = get_occurrence(event_id, year=year, month=month, day=day,
                                               hour=hour, minute=minute, second=second, tzinfo=pytz.utc)
            occurrence.save()
            print(occurrence)
            data = {"url": occurrence.get_absolute_url()}
            return JsonResponse(data)


def guide_profile(request, slug=None):
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
        return HttpResponseRedirect(guide_profile.get_absolute_url)
    context = {"guide_profile": guide_profile,"form":form}
    return render(request, "tour/create_tour_guide.html", context)


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
            object_list = f
            context["object_list"] = object_list
        return context


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
        return context

    def get_current_path(self, request):
        return {'current_path': request.get_full_path()}

    def get_queryset(self, *args, **kwargs):
        qs = super(GuideListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.objects.filter(
                Q(language__icontains=query) | Q(living__icontains=query))
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
        context["query"] = self.request.GET.get("q")
        context["filter_form"] = OccurenceFilterForm(data=self.request.GET or None)
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
            Q(language=query) |	Q(living=query))
            qs = (qs | qs2)
        except:
            pass
        return qs


def booking_email(request, bookings):

    user_name = request.user
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

    return render(request, "forms.html")


class GuideDetailView(DetailView):
    model = Guide

    def get_context_data(self, *args, **kwargs):
        context = super(GuideDetailView, self).get_context_data(*args, **kwargs)

        #________CREATES OR GETS TOUR GUIDES CALANDER__________________
        user = self.get_object().guide_name
        user_calendar = Calendar.objects.get_or_create_calendar_for_object(user, name = str(self.get_object().guide_name))
        context['calendar'] = user_calendar.get_absolute_url
        #________CREATES OR GETS TOUR GUIDES CALANDER__________________

        #________GETS OCCURENCES FOR FOR THE USERS CALANDER____________
        tours = EventRelation.objects.get_events_for_object(user)
        context['tours_list'] = EventRelation.objects.get_events_for_object(user)
        now = datetime.datetime.now()
        tourlist = []
        for tour in tours:
            tourlist.append(tour.get_occurrences(pytz.utc.localize(datetime.datetime(now.year, now.month, now.day)), pytz.utc.localize(datetime.datetime(now.year, 12, 31,))))
        context['tours'] = tourlist
        #________GETS OCCURENCES FOR FOR THE USERS CALANDER____________
        for tour in tourlist:
            for occurrence in tour:
                if occurrence.DoesNotExist:
                    occurrence.guide = self.get_object()
                    occurrence.save()
                else:
                    pass
        context["instance"] = self.get_object()
        context["current_user"] = self.request.user
        context['form'] = GuideBookingForm()

        return context

    def get_current_path(self, request):
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

            booking_email(request, spots_free)

            tours = EventRelation.objects.get_events_for_object(request.user)
            for tour in tours:
                tour_occurrence = tour.get_occurrence(pytz.utc.localize(datetime.datetime(year, month, day, hour, minute, second)))
                tour_occurrence.spots_free -= spots_free
                tour_occurrence.save()
                return HttpResponseRedirect('/1')
        else:
            return super(GuideDetailView, self).post(request, *args, **kwargs)


def tour_map(request):
    import requests
    API_KEY =settings.GOOGLE_MAPS_API_KEY

    if request.GET.get('living') is None:
        latitude = -122.7639851000
        longitude = 45.3840077000
    else:
        address = request.GET.get('living')
        api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, API_KEY))
        api_response_dict = api_response.json()
        if api_response_dict['status'] == 'OK':
            latitude = api_response_dict['results'][0]['geometry']['location']['lat']
            longitude = api_response_dict['results'][0]['geometry']['location']['lng']

    now = datetime.datetime.now()

    tours_list = []
    tour_locations = Event.objects.all()
    #  IMPLEMENT THIS WHEN SEARCHING FOR CITIES - Also filter by Type, Price, Etc... Use Ajax Calls.
    #  print(Event.objects.filter(city='Portland'))
    #  IMPLEMENT THIS WHEN SEARCHING FOR CITIES
    for tour in tour_locations:
        tours_list.append([tour.get_occurrences(pytz.utc.localize(datetime.datetime(now.year, now.month, now.day)), pytz.utc.localize(datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1])))[0]])

    occurrence_list = []
    for tour in tours_list:
        for t in tour:
            # t.save()
            occurrence_list.append(t)

    json_list = serializers.serialize('json', occurrence_list)

    context = {
        "tour_locations": tour_locations,
        "API_KEY": API_KEY,
        "occurrence_list": occurrence_list,
        "json_list": json_list,
        "latitude": latitude,
        "longitude": longitude,
    }
    return render(request, "tour/tour_map.html", context)


class EventViewSet(viewsets.ReadOnlyModelViewSet, View):
    from schedule.serializers import EventSerializer
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user)

    def get(self, request):
        print(request)



# class OccurrenceViewSet(viewsets.ReadOnlyModelViewSet):
#
#     def get_queryset(self):
#         return get_occurrence(self.request.event, year=self.request.year, month=self.request.year, day=self.request.year, hour=self.request.year, minute=self.request.year, seconds=self.request.year)