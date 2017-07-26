from django.contrib import admin
from models import BrewStep, Brew, Probe, TempReading

admin.site.register(BrewStep)
admin.site.register(Brew)
admin.site.register(Probe)
admin.site.register(TempReading)