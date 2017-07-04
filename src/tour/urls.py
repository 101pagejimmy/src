from django.conf.urls import include, url
from django.contrib import admin
from .views import home, create_tour_guide, guide_profile_update, GuideListView, GuideDetailView, OccurrenceListView


urlpatterns = [
	url(r'^$', home, name='home'),
	url(r'^occurrence_listings/$', OccurrenceListView.as_view(), name='occurrence_listings'),
	url(r'^guide_listings/$', GuideListView.as_view(), name='guide_list'),
	url(r'^(?P<pk>\d+)/edit/$', guide_profile_update, name='update'),
	url(r'^(?P<pk>\d+)/$', GuideDetailView.as_view(), name='guide_detail'),
	url(r'^create_tour_guide/$', create_tour_guide, name='create_tour_guide'),
			  ]

