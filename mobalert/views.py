# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from mobalert.models import AccPointsBuffer
# from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return render(request, 
                  'mobalert/home.html',

                 )

def track_loc(request):
    return render(request,
                  'mobalert/track_loc.html',
                 )

def accident_info(request):
    if request.method == 'GET':

        lat = request.GET.get('lat')
        lng = request.GET.get('lng')

        lat = float(lat)
        lng = float(lng)
  
        location = Point(lng, lat, srid=4326)

        danger_zone = AccPointsBuffer.objects.filter(geom__contains=location)

        if danger_zone:
            # create a list with the field's values of the resulted object
            fields = []
            info = 'Alert'
            cause = danger_zone.values_list('title', flat=True).get()
            # str_addr = danger_zone.values_list('str_addr', flat=True).get()
            # accid_num = int(danger_zone.values_list('accid_num', flat=True).get())

            fields.extend([info, cause])
            result = json.dumps(fields)
            # result = "Attention: Danger Zone %s" % danger_zone
        else:
            fields = []
            info = "You are safe"
            cause = ""
            fields.extend([info, cause])
            result = json.dumps(fields)
        return HttpResponse(result,
                            content_type = 'application/json')
