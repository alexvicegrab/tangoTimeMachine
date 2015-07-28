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
        request.POST['event_text'] = 'A new list item'
        
        response = home_page(request)
        
        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_event_text': 'A new list item'}
            )
        self.assertEqual(response.content.decode(), expected_html)

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