from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
#import time

class NewVisitorTest(StaticLiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
    
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
    
    def test_can_open_site_and_create_event(self):
        # Open the homepage
        self.browser.get(self.live_server_url)
        
        # Page header for TTM
        self.assertIn("Tango Ads", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("Tango Ads", header_text)
        
        # Should be able to input a Tango Event into the TTM. 
        inputbox = self.browser.find_element_by_id('id_new_event')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            "Enter a tango event"
        )
        
        # Input an example: "Di Sarli, Carlos"
        inputbox.send_keys("Di Sarli, Carlos")
        inputbox.send_keys(Keys.ENTER)
        
        page1_list_url = self.browser.current_url
        self.assertRegex(page1_list_url, "/pages/.+")
        
        # Update page to list the single Tango Event
        # Now the page should read "Di Sarli, Carlos"
        self.check_for_row_in_list_table("1. Di Sarli, Carlos")
        
        # Should still be able to to add an extra item
        # * "Troilo, Anibal"
        inputbox = self.browser.find_element_by_id('id_new_event')
        inputbox.send_keys("Troilo, Anibal")
        inputbox.send_keys(Keys.ENTER)
        
        # Update page to list both Events
        self.check_for_row_in_list_table("1. Di Sarli, Carlos")
        self.check_for_row_in_list_table("2. Troilo, Anibal")
        
        # A different page should have no events [start by implementing no DB model]
        ## New browser session to ensure no info of page1 comes through cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        # We start adding new events to this page
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_event')
        inputbox.send_keys("D'Arienzo, Juan")
        inputbox.send_keys(Keys.ENTER)
        
        # This page also has a URL
        page2_list_url = self.browser.current_url
        self.assertRegex(page2_list_url, "/pages/.+")
        
        # This should be a different URL
        self.assertNotEqual(page1_list_url, page2_list_url)
        
        # And it does not contain the items in the 1st page, but those in 2nd page
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Di Sarli, Carlos", page_text)
        self.assertIn("D'Arienzo, Juan", page_text)
        
    def test_layout_and_styling(self):
        # Go to home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        
        # Check that the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_event')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta = 5
        )
        
        # Start new list and see that input is centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_event')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta = 5
        )
        