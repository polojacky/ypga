from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from download.models import fieldDescription
from download.forms import registerForm
from django.http import HttpResponse
import csv
from django.utils.encoding import smart_str
from ypga.settings import DOWNLOAD_DIR

# Create your views here.
def index(request):

    return render_to_response('download/index.html',{'DOWNLOAD_DIR':DOWNLOAD_DIR})

# the register page
def register(request):
    if request.session.get('has_registered', False):
        return HttpResponseRedirect('/download/downloadAll/')
    else:
        myForm = registerForm()
        if request.method == 'POST':
            myForm = registerForm(request.POST)
            if myForm.is_valid():
                myForm.save()
                request.session['has_registered'] = True  # set the session
                return HttpResponseRedirect('/download/downloadAll/')
        return render_to_response('download/register.html',locals(),context_instance=RequestContext(request))

def downloadAll(request):
    if request.session.get('has_registered', False):   #registered, may cheat?

        return render_to_response('download/download.html',context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/download/register/')

def gencsv(request):
    print ''

