from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from news.models import news
from browse.models import *
import json
from collections import defaultdict
import codecs
import sys

#index page of the website
def index(request):
    all_news = news.objects.all()[0:4]

    return render_to_response('index.html', {'news':all_news})

#verison too low for browser
def versionUpdate(request):
    return render_to_response('versionUpdate.html')

