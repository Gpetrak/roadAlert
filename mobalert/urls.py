from django.conf.urls import url
from mobalert.views import accident_info

urlpatterns = [
                # url(r'^result/', auto_send, name = 'auto_send'),
                url(r'^data/', accident_info, name='accident_info'),
              ]
