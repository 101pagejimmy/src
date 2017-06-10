from django.conf.urls import include, url
from django.contrib import admin
from .views import home, create_tour_guide, guide_profile_update, GuideListView, GuideDetailView

urlpatterns = [
	url(r'^$', home, name='home'),
	url(r'^guide_listings/$', GuideListView.as_view(), name='guide_list'),
	url(r'^(?P<pk>\d+)/edit/$', guide_profile_update, name='update'),
	url(r'^(?P<pk>\d+)/$', GuideDetailView.as_view(), name='guide_detail'),
	url(r'^create_tour_guide/$', create_tour_guide, name='create_tour_guide'),




#_____________________WORKING________________________________________________________
	
	# url(r'^(?P<slug>[\w-]+)/$', guide_profile, name='guide_profile'),
	# url(r'^(?P<slug>[\w-]+)/edit/$', guide_profile_update, name='update'),
	#url(r'^(?P<pk>\d+)/$', guide_profile, name='guide_profile'),

#_____________________WORKING________________________________________________________

			  ]


			  