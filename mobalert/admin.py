from django.contrib.gis import admin
from mobalert.models import Event

admin.site.register(Event, admin.OSMGeoAdmin)
