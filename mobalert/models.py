# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.forms import ModelForm
from django.forms import Textarea
from datetime import datetime

class Event(models.Model):
    description = models.TextField(max_length=200)
    distance = models.TextField(max_length=200)
    location = models.PointField()
    image = models.ImageField('img', upload_to='images/')
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.description

    def __unicode__(self):
        return self.description or u''

# Build the Textarea
#class EventModelForm(ModelForm):
#    class Meta:
#        model = Event
#        widgets = {
#                'abstract': Textarea(attrs={'cols': 80, 'rows': 20}),
#                }

class AccPointsBuffer(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    title = models.CharField(max_length=80, blank=True, null=True)
    distance = models.BigIntegerField(blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acc_points_buffer'

    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return self.title or u''



