from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_pages(self):
        self.browser.get('http://localhost:8080')

        # homepage
        self.assertIn('Trenord Saga', self.browser.title)
        assert self.browser.find_element_by_id('banner')

        # survey
        self.browser.get('http://localhost:8080/survey')
        self.assertIn('Trenord Saga', self.browser.title)

        # stats
        self.browser.get('http://localhost:8080/stats')
        self.assertIn('Trenord Saga', self.browser.title)

        # about
        self.browser.get('http://localhost:8080/about')
        self.assertIn('Trenord Saga', self.browser.title)
        #self.fail('Finish the test!')

if __name__ == '__main__':
	unittest.main()
