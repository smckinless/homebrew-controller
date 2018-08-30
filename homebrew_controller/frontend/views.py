# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View


# class IndexView(View):
#     template_name = '/frontend/index.html'

def index(request):
    return render(request, 'frontend/index.html')


def brew(request, brew_id):
    return render(request, 'frontend/brew.html')