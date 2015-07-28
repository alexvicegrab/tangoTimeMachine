from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Tango Ads', header_text)
        
        # Should be able to input a Tango Event into the TTM. 
        inputbox = self.browser.find_element_by_id('id_new_event')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a tango event'
        )
        
        # Input an example: "Di Sarli, Carlos"
        inputbox.send_keys('Di Sarli, Carlos')
        inputbox.send_keys(Keys.ENTER)

        # Update page to list the single Tango Event
        # Now the page should read "Di Sarli, Carlos"
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1. Di Sarli, Carlos' for row in rows)
        )
        
        self.fail('Finish the test!')

        # Should still be able to to add an extra item
        # * "Troilo, Anibal"
        
        # Update page to list both Events

        # Refreshing the page should show that the list of events is still there
    
if __name__ == '__main__':
    unittest.main()


    