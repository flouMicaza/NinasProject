
from selenium.webdriver.chrome.webdriver import WebDriver

from Selenium_test.test import InitialData


class SeleniumTest(InitialData):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def login(self, user):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(user.username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('contraseña123')
        self.selenium.find_element_by_id('submit').click()

    def test_muestra_clases(self):
        self. login(user=self.usuaria_profesora)
        primer_curso = self.selenium.find_elements_by_class_name('collapsible-header')[0]



        #self.selenium.find_elements_by_class_name('collapsible-header')[0].click()
        # self.selenium.find_elements_by_xpath("/html/body/main/div[@class='container']/ul[@class=' collection with-header collapsible popout']/li[@class='active']/div[@class='collapsible-body']/a")[0].click()
