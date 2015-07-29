from django.shortcuts import render, redirect
from django.http import HttpResponse
from tangoAds.models import Event, Page

def home_page(request):
    return render(request, 'home.html')
    
def view_page(request):
    events = Event.objects.all()
    return render(request, 'page.html', {'events': events})

def new_page(request):
    page = Page.objects.create()
    Event.objects.create(headline = request.POST['event_headline'], page=page)
    return redirect('/pages/the-only-page-in-the-database/')
