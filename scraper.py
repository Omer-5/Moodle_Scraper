from sys import dont_write_bytecode
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import config as c
from secrets import USERNAME, PASSWORD


class Browser:
    """Browser object that handles all the necessary functions
    """
    def __init__(self) -> None:
        """initialize the browser basic config options to download
        """
        my_firefox_options = FirefoxOptions()
        my_firefox_options.set_preference("browser.download.folderList", 1);
        # Network -> Content-Type
        my_firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain; charset=utf-8; text/csv;application/json;charset=utf-8;application/pdf;text/plain;application/text;text/xml;application/xml;application/msword;text/html")
        my_firefox_options.set_preference("pdfjs.disabled", True)
        # my_firefox_options.set_preference()("browser.download.dir","/home/omer/Downloads")
        # my_firefox_options.add_argument("-private")
        # my_firefox_options.add_argument("--headless")
        # my_firefox_options.add_argument("--browser.helperApps.neverAsk.saveToDisk=application/octet-stream")
        # my_firefox_options.add_argument("--pdfjs.disabled=true")
        # my_firefox_options.add_argument("--pdfjs.enabledCache.state=false")
        self.driver = webdriver.Firefox(options=my_firefox_options)

    def login(self):
        """Go to login URL and log in the url \n
        *DOES NOT HANDLE REDIRECT*
        """
        self.driver.get(c.LOGIN_PAGE_URL)
        self.driver.find_element(By.ID, "username").send_keys(USERNAME)
        self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
        # Logic Button
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/form/input[4]").click()

        sleep(2)
        if self.driver.current_url != c.LOGIN_PAGE_URL:
            print("Logged in")
        else:
            print("login failed")
            self.driver.close()
            raise Exception("Login failed")

    def get_content(self):
        #find out what it locates
        foler_name = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/section[2]/aside/section[1]/div/div/div[1]/div[1]/a").text    

        
if __name__ =='__main__':
    bw = Browser();
    bw.login()
    bw.driver.get(c.HOME_PAGE_URL)
