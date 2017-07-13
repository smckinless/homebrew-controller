from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from homebrew_controller.models import Brew, Probe, TempReading, BrewStep


class TempData(APIView):

    def get(self, request):
        print 'hey'
        return Response([])

    def post(self, request):
        BrewStep.objects.all().delete()
        current_brew_step = BrewStep(name='test')
        current_brew_step.save()
        current_brew = Brew(name='testBrew', current_brew_step=BrewStep.objects.get(name='test'))
        current_brew.is_active = True
        current_brew.save()
        temp_readings = []
        for device in request.data:
            temp = device['temp']
            timestamp = device['timestamp']
            id = device['id']
            try:
                brew = Brew.objects.get(is_active=True)
                brew_step = brew.current_brew_step
                brew.save()
            except Brew.DoesNotExist:
                return Response({'error': 'There are no active brews'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                probe = Probe.objects.get(id=id)
            except Probe.DoesNotExist:
                probe = Probe(id=id)
                probe.save()
            temp_reading = TempReading(brew=brew, brew_step=brew_step, probe=probe, temperature=temp, timestamp=timestamp)
            temp_reading.save()
            temp_readings.append(temp_reading)
            print temp_reading.__dict__
        return Response([])