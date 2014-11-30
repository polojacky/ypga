from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from forms import *
from models import staticticsModel

# Create your views here.
def index(request):
    return render_to_response('about/index.html')

def statistics(request):
    result = staticticsModel.objects.all()
    return render_to_response('about/statistics.html',{'result':result})

def submit(request):
    # AuthorFormSet = modelformset_factory(Author)  we can use factory, but this time we still use ModelForm
    myForm = submitForm()
    if request.method == 'POST':
        myForm = submitForm(request.POST)
        if myForm.is_valid():
            myForm.save()
            return HttpResponseRedirect('/about/submitHistory')

    return render_to_response('about/submit.html',locals(),context_instance=RequestContext(request))

def contact(request):
    myForm = contactForm()
    if request.method == 'POST':
        myForm = contactForm(request.POST)
        if myForm.is_valid():
            myForm.save()
            # send a mail to administrator
            # get administrator email from settings.py
            # title = myForm.cleaned_data['title']
            # email = myForm.cleaned_data['email']
            # content = myForm.cleaned_data['content']
            # send_mail(title, content, email, [ADMIN_EMAIL], fail_silently=True)
            return HttpResponseRedirect('/about/thanks/')

    return render_to_response('about/contact.html',locals(),context_instance=RequestContext(request))

def copyright(request):
    return render_to_response('about/copyright.html')

def external(request):
    return render_to_response('about/external.html')

def thanks(request):
    return render_to_response('about/thanks.html')

def lab(request):
    return render_to_response('about/lab.html')