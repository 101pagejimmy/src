from django.contrib import admin
from .models import ReservationDay, Holiday


admin.site.register(ReservationDay)
admin.site.register(Holiday)