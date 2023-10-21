from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from fonbet import Fonbet
from leon import Leon
from onexbet import Onexbet


class Forks:
    def __init__(self):
        self.browser = self.__init_browser()
        self.fonbet = Fonbet()
        self.leon = Leon()
        # self.onexbet = Onexbet(self.browser)

    def run(self):
        self.fonbet.run()
        # self.leon.run()
        # self.onexbet.run()

    def __init_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0')
        browser = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
        browser.implicitly_wait(10)
        return browser