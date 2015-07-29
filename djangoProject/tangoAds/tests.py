from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from tangoAds.views import home_page
from tangoAds.models import Event

class HomePageTest(TestCase):   
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        
        self.assertEqual(found.func, home_page)
    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        
        response = home_page(request)
        expected_html = render_to_string('home.html')
        
        self.assertEqual(response.content.decode(), expected_html)
    
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['event_headline'] = 'A new event headline'
        
        response = home_page(request)
        
        self.assertEqual(Event.objects.count(), 1)
        new_event = Event.objects.first()
        self.assertEqual(new_event.headline, 'A new event headline')
        
    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['event_headline'] = 'A new event headline'
        
        response = home_page(request)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/pages/the-only-page-in-the-database/')
    
class EventModelTest(TestCase):
    def test_saving_and_retrieving_events(self):
        first_event = Event()
        first_event.headline = 'First headline'
        first_event.save()
        
        second_event = Event()
        second_event.headline = 'Second headline'
        second_event.save()
        
        saved_events = Event.objects.all()
        self.assertEqual(saved_events.count(), 2)
        
        first_saved_event = saved_events[0]
        second_saved_event = saved_events[1]
        self.assertEqual(first_saved_event.headline, 'First headline')
        self.assertEqual(second_saved_event.headline, 'Second headline')
    
    def test_home_page_only_saves_events_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Event.objects.count(), 0)

class EventViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/pages/the-only-page-in-the-database/')
        self.assertTemplateUsed(response, 'page.html')
    
    def test_displays_all_events(self):
        Event.objects.create(headline="Event one")
        Event.objects.create(headline="Event two")
        
        response = self.client.get('/pages/the-only-page-in-the-database/')
        
        self.assertContains(response, "Event one")
        self.assertContains(response, "Event two")
    
    