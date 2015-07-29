from django.shortcuts import render, redirect
from django.http import HttpResponse
from tangoAds.models import Event

def home_page(request):
    if request.method == 'POST':
        Event.objects.create(headline = request.POST['event_headline'])
        return redirect('/')
    
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})
    
    
