# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, QueryDict
from django.template.context_processors import request
from django.template import loader

from .models import ufHistory

# All imports for retriving data
from .bcentralProcessor import bcentralProcessor


def index(request):
    return render(request, 'uf/index.html')

def listUfHistory(request):
    ufList = ufHistory.objects.order_by('-publishedDate').all()
    return render(request, 'uf/list.html', {'ufList': ufList})

def price(request):    
    params = bcentralProcessor.computeUfFromQueryString(request.GET)
    
    if params['ufDate'] and params['inputValue']:   # Both are not None
        if params['ufHistoricalValue']:
            return render(request, 'uf/price.html', params)
        else:
            return HttpResponse("Unable to Find Historical UF record")
    else:
        return HttpResponse("Unable to Parse Query String.<br>Parameters are case sensitive.<br>Make sure 'value' is a float and 'date' is YYYYMMDD" )

def retrieveUF(request):
    bcentralproc = bcentralProcessor()
    if bcentralproc.retrieveUFDataWithSelenium() == 1:
        return HttpResponse("Success")
    else:
        return HttpResponse("Unable to retrieve Data")

def clearDB(request):
    bcentralProc = bcentralProcessor()
    bcentralProc.clearDB()    
    return HttpResponse("Database Cleared")
    
