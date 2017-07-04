from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from tour.views import create_tour_guide, GuideDetail

#_______IN THE WORKS FOR REST_FRAMEWORK___________________
# router = DefaultRouter()
# router.register(r'guidesdetailpage', GuideDetail)
#_______IN THE WORKS FOR REST_FRAMEWORK___________________


urlpatterns = [
#_______IN THE WORKS FOR REST_FRAMEWORK___________________
	# url(r'^', include(router.urls)),
#_______IN THE WORKS FOR REST_FRAMEWORK___________________
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^calendar/', include('schedule.urls')),
    url(r'^review/', include('review.urls')),
    url(r'^create_tour_guide/$', create_tour_guide, name='create_tour_guide'),
    url(r'^', include('tour.urls', namespace="tour")),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    