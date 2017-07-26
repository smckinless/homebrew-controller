"""homebrew_controller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from api_views import TempData, SetCurrentBrewStep, GetAllBrewsAPI, GetAllTempData
from views import IndexView, BrewingView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^temp_data/$', TempData.as_view()),
    url(r'^$', IndexView.as_view()),
    url(r'^set_step/$', SetCurrentBrewStep.as_view()),
    url(r'^brew/$', BrewingView.as_view()),
    url(r'^get/all/brews/$', GetAllBrewsAPI.as_view()),
    url(r'^get/temp_data/$', GetAllTempData.as_view()),
]
