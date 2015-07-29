from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from tangoAds.views import home_page
from tangoAds.models import Event, Page

class HomePageTest(TestCase):   
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        
        self.assertEqual(found.func, home_page)
    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        
        response = home_page(request)
        expected_html = render_to_string('home.html')
        
        self.assertEqual(response.content.decode(), expected_html)
    
    
    
class PageAndEventModelTest(TestCase):
    def test_saving_and_retrieving_events(self):
        page = Page()
        page.save()
        
        first_event = Event()
        first_event.headline = 'First headline'
        first_event.page = page
        first_event.save()
        
        second_event = Event()
        second_event.headline = 'Second headline'
        second_event.page = page
        second_event.save()
        
        saved_page = Page.objects.first()
        self.assertEqual(saved_page, page)
        
        saved_events = Event.objects.all()
        self.assertEqual(saved_events.count(), 2)
        
        first_saved_event = saved_events[0]
        second_saved_event = saved_events[1]
        self.assertEqual(first_saved_event.headline, 'First headline')
        self.assertEqual(first_saved_event.page, page)
        self.assertEqual(second_saved_event.headline, 'Second headline')
        self.assertEqual(second_saved_event.page, page)
    

class PageViewTest(TestCase):
    def test_passes_correct_page_to_template(self):
        other_page = Page.objects.create()
        correct_page = Page.objects.create()
        response = self.client.get('/pages/%d/' % (correct_page.id,))
        self.assertEqual(response.context['page'], correct_page)
        
    def test_uses_list_template(self):
        page = Page.objects.create()
        response = self.client.get('/pages/%d/' % (page.id,))
        self.assertTemplateUsed(response, 'page.html')
    
    def test_displays_only_events_for_that_page(self):
        correct_page = Page.objects.create()
        Event.objects.create(headline="Event one", page=correct_page)
        Event.objects.create(headline="Event two", page=correct_page)
        other_page = Page.objects.create()
        Event.objects.create(headline="Event three", page=other_page)
        Event.objects.create(headline="Event four", page=other_page)
        
        response = self.client.get('/pages/%d/' % (correct_page.id,) )
        
        self.assertContains(response, "Event one")
        self.assertContains(response, "Event two")
        self.assertNotContains(response, "Event three")
        self.assertNotContains(response, "Event four")

class NewPageTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_page(self):
        other_page = Page.objects.create()
        correct_page = Page.objects.create()
        
        self.client.post(
            '/pages/%d/add_event' % (correct_page.id,),
            data = {'event_headline': "A new event headline"}
        )
        
        self.assertEqual(Event.objects.count(), 1)
        new_event = Event.objects.first()
        self.assertEqual(new_event.headline, "A new event headline")
        self.assertEqual(new_event.page, correct_page)
    
    def test_redirects_to_page_view(self):
        other_page = Page.objects.create()
        correct_page = Page.objects.create()
        
        response = self.client.post(
            '/pages/%d/add_event' % (correct_page.id,),
            data = {'event_headline': "A new event for an existing page"}
        )
        
        self.assertRedirects(response, '/pages/%d/' % (correct_page.id,))
    
    def test_saving_a_POST_request(self):
        self.client.post(
            '/pages/new',
            data={'event_headline': 'A new event headline'}
        )
    
        self.assertEqual(Event.objects.count(), 1)
        new_event = Event.objects.first()
        self.assertEqual(new_event.headline, 'A new event headline')
        
    def test_redirects_after_POST(self):
        response = self.client.post(
            '/pages/new',
            data={'event_headline': 'A new event headline'}
        )
        page = Page.objects.first()
        self.assertRedirects(response, '/pages/%d/' % (page.id,))