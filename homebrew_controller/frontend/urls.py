from django.conf.urls import url
from views import index, brew

urlpatterns = [
    url('^$', index),
    url('^brew/(?P<brew_id>[0-9])/$', brew)
]