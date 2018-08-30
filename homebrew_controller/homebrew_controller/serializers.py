from rest_framework import serializers
from models import TempReading, BrewStep, Brew, Probe


class BrewStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrewStep
        fields = '__all__'


class TempReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempReading
        fields = '__all__'


class BrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brew
        fields = '__all__'


class ProbeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probe
        fields = '__all__'
