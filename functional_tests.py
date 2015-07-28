from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
    
    def test_can_open_site_and_create_event(self):
        # Open the homepage
        self.browser.get('http://localhost:8000')

        # Page header for TTM
        self.assertIn('Tango Ads', self.browser.title)
        
        # Should be able to input a Tango Event into the TTM. Input an example:
        # * "Di Sarli, Carlos"

        # Update page to list the single Tango Event
        # Now the page should read "Di Sarli, Carlos"

        # Should still be able to to add an extra item
        # * "Troilo, Anibal"

        # Update page to list both Events

        # Refreshing the page should show that the list of events is still there
    
if __name__ == '__main__':
    unittest.main()


    