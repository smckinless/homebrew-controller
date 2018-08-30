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
from api_views import CreateTempReadingAPI, CreateBrewStepAPI, CreateProbeAPI, SetCurrentBrewStep, GetAllBrewsAPI, SetBrewStatus, TempReadingsForMashStep, TempReadingsForBoilStep, TempReadingsForFermentationStep, CreateBrewAPI, GetBrewAPI
from views import IndexView, BrewingView, AllBrewsView, BrewView

urlpatterns = [
    url(r'^', include('frontend.urls', namespace='frontend')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^temp_data/$', CreateTempReadingAPI.as_view()),
    # url(r'^$', IndexView.as_view()),
    url(r'^set_step/$', SetCurrentBrewStep.as_view()),
    url(r'^brew/$', BrewingView.as_view()),
    url(r'^get/all/brews/$', GetAllBrewsAPI.as_view()),
    url(r'^all_brews/$', AllBrewsView.as_view()),
    url(r'^brew/(?P<brew_id>[0-9])/$', BrewView.as_view()),
    url(r'^api/brew/(?P<id>[0-9])/$', GetBrewAPI.as_view()),
    url(r'^brew/set_status/$', SetBrewStatus.as_view()),
    url(r'^api/brew/(?P<brew_id>[0-9])/mash/$', TempReadingsForMashStep.as_view()),
    url(r'^api/brew/(?P<brew_id>[0-9])/boil/$', TempReadingsForBoilStep.as_view()),
    url(r'^api/brew/(?P<brew_id>[0-9])/fermentation/$', TempReadingsForFermentationStep.as_view()),
    url(r'^brew/create/$', CreateBrewAPI.as_view()),
    url(r'^probe/create/$', CreateProbeAPI.as_view()),
    url(r'^brew-step/create/$', CreateBrewStepAPI.as_view()),
]
