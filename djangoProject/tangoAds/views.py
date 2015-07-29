from django.shortcuts import render, redirect
from django.http import HttpResponse
from tangoAds.models import Event

def home_page(request):
    if request.method == 'POST':
        Event.objects.create(headline = request.POST['event_headline'])
        return redirect('/pages/the-only-page-in-the-database/')
        
    return render(request, 'home.html')
    
def view_page(request):
    events = Event.objects.all()
    return render(request, 'page.html', {'events': events})
