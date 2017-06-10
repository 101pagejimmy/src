from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from tour.views import guide_profile, landing, create_tour_guide, create_post

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^booking/', include('booking.urls')),
    url(r'^calendar/', include('schedule.urls')),
    #url(r'^reservations/', include('reservations.urls')),
    url(r'^review/', include('review.urls')),
    url(r'^landing/$', landing, name='landing'),
    url(r'^create_tour_guide/$', create_tour_guide, name='create_tour_guide'),
    url(r'^', include('tour.urls', namespace="tour")),

    #_____________________IN THE WORKS________________________________________________________
    url(r'^create_post/$', create_post, name='create_post'),
    #_____________________IN THE WORKS________________________________________________________
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    