from django.shortcuts import render, redirect
from django.http import HttpResponse
from tangoAds.models import Event, Page

def home_page(request):
    return render(request, 'home.html')
    
def view_page(request, page_id):
    page = Page.objects.get(id=page_id)
    return render(request, 'page.html', {'page': page})

def new_page(request):
    page = Page.objects.create()
    Event.objects.create(headline = request.POST['event_headline'], page=page)
    return redirect('/pages/%d/' % (page.id,))

def add_event(request, page_id):
    page = Page.objects.get(id=page_id)
    Event.objects.create(headline = request.POST['event_headline'], page=page)
    return redirect('/pages/%d/' % (page.id,))