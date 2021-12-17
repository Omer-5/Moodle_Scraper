from sys import dont_write_bytecode
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from secrets import USERNAME, PASSWORD


class Browser:
    """initialize the browser basic config options to downlaod
    """
    def __init__(self) -> None:
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
        self.driver.find_element(By.ID, "username").send_keys(USERNAME)
        self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
        # Logic Button
        self.driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[1]/form/input[5]").click()

        sleep(2)
        if "https://md.hit.ac.il/" == self.driver.title:
            print("Logged in")
        else:
            print("Please log in")
            # self.driver.close()
            sys.exit()

    def refresh_page(self):
        self.driver.refresh()
        self.driver.switch_to.alert.accept() # dismisses the alert of a refresh in login page
        sleep(2)
        if "https://is.hit.ac.il" in self.driver.current_url:
            print("need to login")
            self.login()
    
    def get_content(self):
        #find out what it locates
        foler_name = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/section[2]/aside/section[1]/div/div/div[1]/div[1]/a").text    

        
if __name__ =='__main__':
    bw = Browser();
    bw.driver.get("https://md.hit.ac.il/")

    if "https://md.hit.ac.il/" != bw.driver.title:
        bw.login()