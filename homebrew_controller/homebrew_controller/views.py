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


def get_temp_readings_for_brew(brew):
    probes = Probe.objects.all()
    temp_readings_dict = {}
    for probe in probes:
        temp_readings_dict[probe.id] = []
        temp_probe_list = []
        temp_readings = TempReading.objects.filter(brew=brew, brew_step=brew.current_brew_step, probe=probe)
        for temp_reading in temp_readings:
            temp_probe_list.append({'timestamp': temp_reading.timestamp.isoformat(),
                                       'temperature': temp_reading.temperature})
        temp_readings_dict[probe.id] = temp_probe_list

    return temp_readings_dict


class BrewingView(View):
    template_name = 'brewing.html'

    def get(self, request):
        context = {}
        current_brew = Brew.objects.get(is_active=True)
        context['current_brew'] = current_brew
        # TODO: Organize temp readings by probe to create a chart for each probe
        probes = Probe.objects.all()
        temp_readings_dict = get_temp_readings_for_brew(current_brew)
        context[u'temp_readings'] = json.dumps(temp_readings_dict)
        context[u'probes'] = probes
        return render(request, self.template_name, context)


class AllBrewsView(View):
    template_name = 'all_brews.html'

    def get(self, request):
        context = {}
        # Get all non-current brews
        brews = Brew.objects.filter(is_active=False)
        context[u'brews'] = brews
        return render(request, self.template_name, context)


class BrewView(View):
    template_name = 'brew.html'

    def get(self, request, brew_id):
        context = {}
        brew = Brew.objects.get(id=brew_id) if brew_id else None
        probes = Probe.objects.all()
        temp_readings = get_temp_readings_for_brew(brew)
        context[u'brew'] = brew
        context[u'temp_readings'] = temp_readings
        context[u'probes'] = probes
        return render(request, self.template_name, context)