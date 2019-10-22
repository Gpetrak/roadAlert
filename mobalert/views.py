# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from mobalert.models import AccPointsBuffer
# from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers

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

            # serializing many results in a json object
            #cause = serializers.serialize ('json',
            #                                danger_zone,
            #                                fields=('title')
            #                              )
            # I use filter() instead of get() because it is possible to more than one object for one location
            cause = danger_zone.values_list('title', flat=True).filter()
  
            # First I add the info value to the fields list
            fields.append(info)
            # After that I add all the values from title field that django detected
            for i in cause:
                fields.append(i)    
            
            result = json.dumps(fields)
            
        else:
            fields = []
            info = "You are safe"
            cause = ""
            fields.extend([info, cause])
            result = json.dumps(fields)
        return HttpResponse(result,
                            content_type = 'application/json')
