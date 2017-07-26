from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import MultipleObjectsReturned

from homebrew_controller.models import Brew, Probe, TempReading, BrewStep


class TempData(APIView):
    """
    Creates a temp reading object for the given brew and brew step.
    """

    def get(self, request):
        print 'hey'
        return Response([])

    def post(self, request):
        # BrewStep.objects.all().delete()
        # current_brew_step = BrewStep(name='test')
        # current_brew_step.save()
        # current_brew = Brew(name='testBrew', current_brew_step=BrewStep.objects.get(name='test'))
        # current_brew.is_active = True
        # current_brew.save()
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


class GetAllTempData(APIView):
    """
    Gets all temp data for given brew, brew step, and probe.
    """
    def get(self, request):
        brew = request.GET.get('brew')
        brew_step = request.GET.get('brew_step')
        #TODO: Filter by probe if probe is passed in
        probe = request.GET.get('probe')
        temp_readings = TempReading.objects.filter(brew=brew, brew_step=brew_step)
        temp_readings_list = []
        for temp_reading in temp_readings:
            temp_readings_list.append({'x': temp_reading.timestamp.isoformat(),
                                       'y': temp_reading.temperature})
        return Response({'data': temp_readings_list}, status=status.HTTP_200_OK)

class SetCurrentBrewStep(APIView):
    """
    Sets the given brew step as the current brew step for the active brew.
    """

    def post(self, request):
        step_name = request.data['step_name']
        try:
            current_brew = Brew.objects.get(is_active=True)
        except Brew.DoesNotExist:
            return Response({'error': 'There are no active brews.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            step = BrewStep.objects.get(name=step_name)
        except BrewStep.DoesNotExist:
            return Response({'error': 'This is not a brew step.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except MultipleObjectsReturned:
            return Response({'error': 'Multiple instances of this brew step exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        current_brew.update(current_brew_step=step)
        return Response({'data': 'Fermentation step %s added to brew.' % step.name}, status=status.HTTP_200_OK)


class GetAllBrewsAPI(APIView):
    """
    Gets all the previously completed brews.
    """
    def get(self, request):
        all_brews = Brew.objects.filter(is_active=False)
        context = {'brews': all_brews}
        return Response(context, status=status.HTTP_200_OK)