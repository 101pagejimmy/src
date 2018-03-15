from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from tour.views import create_tour_guide, tour_booker, calendar_event_creator, EventViewSet
from orders.views import (AddressSelectFormView, UserAddressCreateView, OrderList, OrderDetail)
from carts.views import CartView, ItemCountView, CheckoutView, CheckoutFinalView

router = routers.DefaultRouter()
router.register(r'events', EventViewSet, 'event')

urlpatterns = [
    url(r'^', include('tour.urls', namespace="tour")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^calendar/', include('schedule.urls')),
    url(r'^review/', include('review.urls')),
    url(r'^create_tour_guide/$', create_tour_guide, name='create_tour_guide'),
    url(r'^tour_booker/$', tour_booker, name='tour_booker'),
    url(r'^calendar_event_creator/$', calendar_event_creator, name='calendar_event_creator'),
    #CART
    url(r'^orders/$', OrderList.as_view(), name='orders'),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetail.as_view(), name='order_detail'),
    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^cart/count/$', ItemCountView.as_view(), name='item_count'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^checkout/address/$', AddressSelectFormView.as_view(), name='order_address'),
    url(r'^checkout/address/add/$', UserAddressCreateView.as_view(), name='user_address_create'),
    url(r'^checkout/final/$', CheckoutFinalView.as_view(), name='checkout_final'),

    url(r'^api/', include(router.urls, namespace='api')),

]
admin.site.site_header = 'SpotOn Tours Administration'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
