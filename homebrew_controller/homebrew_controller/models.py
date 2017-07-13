from django.db import models

class BrewStep(models.Model):
    name = models.CharField(max_length=256)

class Brew(models.Model):
    name = models.CharField(max_length=256)
    current_brew_step = models.ForeignKey(BrewStep, null=True)
    is_active = models.BooleanField(default=False)

class Probe(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    location = models.CharField(max_length=256)

class TempReading(models.Model):
    brew = models.ForeignKey(Brew)
    brew_step = models.ForeignKey(BrewStep)
    temperature = models.FloatField()
    timestamp = models.DateTimeField()
    probe = models.ForeignKey(Probe)