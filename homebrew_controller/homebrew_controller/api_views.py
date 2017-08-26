from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import MultipleObjectsReturned
from django.forms.models import model_to_dict

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
        if probe:
            try:
                probe = Probe.objects.get(id=probe)
            except Probe.DoesNotExist:
                return Response({'error': 'Invalid probe id'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            temp_readings = TempReading.objects.filter(brew=brew, brew_step=brew_step, probe=probe)
        else:
            #temp_readings = TempReading.objects.filter(brew=brew, brew_step=brew_step)
            return Response({'error': 'No probe specified'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = {}
        temp_readings_list = []
        for temp_reading in temp_readings:
            temp_readings_list.append({'x': temp_reading.timestamp.isoformat(),
                                       'y': temp_reading.temperature})
        data[probe.id] = temp_readings_list
        return Response({'data': data}, status=status.HTTP_200_OK)


class SetCurrentBrewStep(APIView):
    """
    Sets the given brew step as the current brew step for the active brew.
    """

    def get(self, request):
        try:
            current_brew = Brew.objects.get(is_active=True)
        except Brew.DoesNotExist:
            return Response({'error': 'There are no active brews.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        current_step = current_brew.current_brew_step
        brew_steps = BrewStep.objects.exclude(name=current_step.name)
        serialized_brew_steps = []
        for brew in brew_steps:
            brew = model_to_dict(brew)
            serialized_brew_steps.append(brew)
        if brew_steps:
            return Response({'data': serialized_brew_steps}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'There are no remaining brew steps'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        current_brew.current_brew_step = step
        current_brew.save()
        return Response({'data': 'Brewing step %s added to brew.' % step.name}, status=status.HTTP_200_OK)


class GetAllBrewsAPI(APIView):
    """
    Gets all the previously completed brews.
    """
    def get(self, request):
        all_brews = Brew.objects.filter(is_active=False)
        context = {'brews': all_brews}
        return Response(context, status=status.HTTP_200_OK)


class SetBrewStatus(APIView):
    """
    Sets the current brew to inactive/active if there is one.
    """
    def post(self, request):
        brew = request.data['brew']
        is_active = request.data['is_active']
        if brew is not None and is_active is not None:
            brew = Brew.objects.get(id=brew)
            brew.is_active = is_active
            brew.save()
            return Response({'data': 'Brew set to inactive'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Brew id and/or is_active not added to request'}, status=status.HTTP_400_BAD_REQUEST)