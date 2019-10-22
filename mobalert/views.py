# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from mobalert.models import AccPointsBuffer, Event
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
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
    '''
    It gets user location and checks if she/he is in a dangerous area or not. 
    After that, send her/him a response
    '''
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


@csrf_exempt 
def datastore(request):
    '''
    It receives the event's info that a user sends and 
    stores the event in the spatial database as a polygon,
    creating a buffer from the coordinates that the user sends
    taking in to account the buffer distance.
    '''

    if request.method == 'POST':
        # convert json data to python dictionary
        desc_loc =json.loads(request.body)
        description = desc_loc['desc']
        distance = desc_loc['dist']
        latitude = desc_loc['lat']
        longitude = desc_loc['lon']
        
        location = Point(longitude, latitude, srid=4326)
        
        if request.FILES.get('image'):
            # image store
            myimage = request.FILES.get('image')
            fs = FileSystemStorage()
            filename = fs.save(myimage.name, myimage)
            uploaded_file_url = fs.url(filename)
        
            e1 = Event(description = description,
                       distance = distance,
                       location = location,
                       image = image)

        else:
            e1 = Event(description = description,
                       distance = distance,
                       location = location,
                      )


        e1.save()
     
        # check if e1 saved
        if e1.pk is None:
            return HttpResponse("Upload failed")
        else:
            return HttpResponse("Success")
