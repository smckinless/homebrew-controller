from django.views import View
from django.shortcuts import render

from homebrew_controller.models import Brew, TempReading


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name, {})

class BrewingView(View):
    template_name = 'brewing.html'

    def get(self, request):
        context = {}
        current_brew = Brew.objects.get(is_active=True)
        context['current_brew'] = current_brew
        # TODO: Organize temp readings by probe to create a chart for each probe
        temp_readings = TempReading.objects.filter(brew=current_brew, brew_step=current_brew.current_brew_step)
        temp_readings_list = []
        for temp_reading in temp_readings:
            temp_readings_list.append({'timestamp': temp_reading.timestamp,
                                       'temperature': temp_reading.temperature})
        context['temp_readings'] = temp_readings_list
        return render(request, self.template_name, context)