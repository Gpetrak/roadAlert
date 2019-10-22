from django.contrib.gis import admin
from mobalert.models import Event, AccPointsBuffer

admin.site.register(Event, admin.OSMGeoAdmin)
admin.site.register(AccPointsBuffer)
