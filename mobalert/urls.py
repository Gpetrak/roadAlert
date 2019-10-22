from django.conf.urls import url
from mobalert.views import home, accident_info, track_loc, datastore

urlpatterns = [
                url(r'mobalert/', home, name='home'),
                url(r'track_loc/', track_loc, name='track_loc'), 
                # url(r'^result/', auto_send, name = 'auto_send'),
                url(r'^data/', accident_info, name='accident_info'),
                url(r'^results/', datastore, name = 'datastore'),
              ]
