from django.db import models

class Brew(models.Model):
    name = models.CharField(max_length=256)

class BrewStep(models.Model):
    name = models.CharField(max_length=256)

class Probe(models.Model):
    location = models.CharField(max_length=256)

class TempReading(models.Model):
    brew = models.ForeignKey(Brew)
    brew_step = models.ForeignKey(BrewStep)
    temperature = models.FloatField()
    timestamp = models.DateTimeField()
    probe = models.ForeignKey(Probe)