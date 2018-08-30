from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.core.exceptions import MultipleObjectsReturned
from django.forms.models import model_to_dict

from homebrew_controller.models import Brew, Probe, TempReading, BrewStep
from homebrew_controller.model.BrewStepChoices import BrewStepChoices
from homebrew_controller.serializers import TempReadingSerializer, BrewSerializer, ProbeSerializer, BrewStepSerializer


class CreateTempReadingAPI(generics.CreateAPIView):
    """
    Creates a temp reading object for the given brew and brew step.
    """
    queryset = TempReading.objects.all()
    serializer_class = TempReadingSerializer


class CreateBrewAPI(generics.CreateAPIView):
    queryset = Brew.objects.all()
    serializer_class = BrewSerializer


class CreateProbeAPI(generics.CreateAPIView):
    queryset = Probe.objects.all()
    serializer_class = ProbeSerializer


class ActiveBrewAPI(generics.RetrieveAPIView):
    queryset = Brew.objects.all()
    serializer_class = BrewSerializer

    def get_queryset(self):
        return Brew.objects.get(is_active=True)


class ActiveBrewStepForBrewAPI(generics.RetrieveAPIView):
    queryset = BrewStep.objects.all()
    serializer_class = BrewStepSerializer

    def get_queryset(self):
        return BrewStep.objects.get(is_active=True)


class CreateBrewStepAPI(generics.CreateAPIView):
    queryset = BrewStep.objects.all()
    serializer_class = BrewStepSerializer


class SetCurrentBrewStep(APIView):
    """
    Sets the given brew step as the current brew step for the active brew.
    """

    # def get(self, request):
    #     # try:
    #     #     current_brew = Brew.objects.get(is_active=True)
    #     # except Brew.DoesNotExist:
    #     #     return Response({'error': 'There are no active brews.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     current_step = BrewStep.objects.get(is_active=True)
    #     brew_steps = BrewStep.objects.exclude(name=current_step.name)
    #     serialized_brew_steps = []
    #     for brew in brew_steps:
    #         brew = model_to_dict(brew)
    #         serialized_brew_steps.append(brew)
    #     if brew_steps:
    #         return Response({'data': serialized_brew_steps}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'error': 'There are no remaining brew steps'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        step = BrewStep(value=request.data['step_name'])
        current_brew_step = BrewStep.objects.filter(is_active=True)
        if current_brew_step:
            current_brew_step.update(is_active=False)
        try:
            current_brew_step = BrewStep.objects.get(id=step.value)
        except BrewStep.DoesNotExist:
            return Response({'error': 'This is not a brew step.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except MultipleObjectsReturned:
            return Response({'error': 'Multiple instances of this brew step exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        current_brew_step.update(is_active=True)
        return Response({'data': 'Brewing step %s added to brew.' % step}, status=status.HTTP_200_OK)


class GetAllBrewsAPI(generics.ListAPIView):
    """
    Gets all the previously completed brews.
    """
    queryset = Brew.objects.all()
    serializer_class = BrewSerializer

    def get_queryset(self):
        return Brew.objects.filter(is_active=False)


class GetBrewAPI(generics.RetrieveUpdateAPIView):
    """
    Gets Brew based on given id.
    """
    queryset = Brew.objects.all()
    serializer_class = BrewSerializer
    lookup_field = 'id'

    def get_queryset(self):
        print self.kwargs['id']
        return Brew.objects.filter(id=self.kwargs['id'])


class SetBrewStatus(APIView):
    """
    Sets the current brew to inactive/active if there is one.
    """
    def post(self, request):
        brew = request.data['brew']
        is_active = request.data['is_active']
        if brew and is_active:
            brew = Brew.objects.get(id=brew)
            brew.is_active = is_active
            brew.save()
            return Response({'data': 'Brew set to inactive'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Brew id and/or is_active not added to request'}, status=status.HTTP_400_BAD_REQUEST)


class TempReadingsForMashStep(generics.ListAPIView):
    """
    Get info on mash step
    """
    serializer_class = TempReadingSerializer

    def get_queryset(self):
        brew_id = self.kwargs['brew_id']
        return TempReading.objects.filter(brew__id=brew_id, brew_step=BrewStepChoices.MASH.value)


class TempReadingsForBoilStep(generics.ListAPIView):
    """
    Get info on boil step
    """
    serializer_class = TempReadingSerializer

    def get_queryset(self):
        brew_id = self.kwargs['brew_id']
        return TempReading.objects.filter(brew__id=brew_id, brew_step=BrewStepChoices.BOIL.value)


class TempReadingsForFermentationStep(generics.ListAPIView):
    """
    Get info on fermentation step
    """
    serializer_class = TempReadingSerializer

    def get_queryset(self):
        brew_id = self.kwargs['brew_id']
        return TempReading.objects.filter(brew__id=brew_id, brew_step=BrewStepChoices.FERMENTATION.value)