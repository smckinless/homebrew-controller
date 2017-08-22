from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json

from homebrew_controller.models import Brew, TempReading, Probe


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        brew_name = request.POST.get('brew_name')
        if brew_name and not Brew.objects.filter(is_active=True):
            new_brew = Brew(name=brew_name)
            new_brew.save()
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("No brew name passed in or already active brews")


class BrewingView(View):
    template_name = 'brewing.html'

    def get(self, request):
        context = {}
        current_brew = Brew.objects.get(is_active=True)
        context['current_brew'] = current_brew
        # TODO: Organize temp readings by probe to create a chart for each probe
        probes = Probe.objects.all()
        temp_readings_dict = {}
        for probe in probes:
            temp_readings_dict[probe.id] = []
            temp_probe_list = []
            temp_readings = TempReading.objects.filter(brew=current_brew, brew_step=current_brew.current_brew_step, probe=probe)
            for temp_reading in temp_readings:
                temp_probe_list.append({'timestamp': temp_reading.timestamp.isoformat(),
                                           'temperature': temp_reading.temperature})
            temp_readings_dict[probe.id] = temp_probe_list
        print temp_readings_dict
        context[u'temp_readings'] = json.dumps(temp_readings_dict)
        context[u'probes'] = probes
        return render(request, self.template_name, context)