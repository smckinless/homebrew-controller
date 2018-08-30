from django.db import models


class BrewStep(models.Model):
    is_active = models.BooleanField(default=False)
    name = models.CharField(unique=True, max_length=256)


class Brew(models.Model):
    name = models.CharField(max_length=256)
    is_active = models.BooleanField(default=False)
    recipe_list = models.TextField(null=True)
    flavor_profile = models.TextField(null=True)
    other_notes = models.TextField(null=True)


class Probe(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    location = models.CharField(max_length=256)


class TempReading(models.Model):
    brew = models.ForeignKey(Brew)
    brew_step = models.ForeignKey(BrewStep)
    temperature = models.FloatField()
    timestamp = models.DateTimeField()
    probe = models.ForeignKey(Probe)