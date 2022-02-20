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
        my_firefox_options.set_preference("intl.accept_languages", "locale-of-choice")

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
        self.driver.find_element(By.XPATH, c.LOGIN_BUTTON).click()

        sleep(2)
        if self.driver.current_url != c.LOGIN_PAGE_URL:
            print("Logged in")
        else:
            print("login failed")
            self.driver.close()
            raise Exception("Login failed")

    def course_dispatcher(self):
        """ Scan the page for all the relevant courses and send them to be parsed
            assume logged in and redirected to home page
        """
        all_courses_div = self.driver.find_element(By.XPATH, c.ALL_COURSES_DIV)
        courses = all_courses_div.find_elements(By.TAG_NAME,"li")

        for course in courses:
            if(course.text != ""):
                course_name = course.text.replace("קורס","")
                course_url = course.find_element(By.TAG_NAME,"a").get_attribute('href')
                # send to strage class - check if table exist and switch to it
                self.course_extractor(course_name,course_url)
            break # remove after testing
        self.driver.close()

    def course_extractor(self, course_name, course_url):
        """ extracting all crouse content

        Args:
            course_name (string): hebrew course name
            course_url (string): course url
        """
        self.driver.get(course_url)

        sections = self.driver.find_elements(By.CLASS_NAME,c.DIV_SECTION_CLASS)

        for section in sections:
            section_extractor(self, section)


    def section_extractor(self, section):
        section_name = section.find_element(By.TAG_NAME,"h3").text
        
        section_ul = section.find_elements(By.CLASS_NAME, c.UL_CLASS_NAME)
        if len(section_ul) > 0:
            sections_li = section_ul[0].find_elements(By.CLASS_NAME, c.LI_CLASS_NAME)

            for li in sections_li:
                file_link_url_raw = li.find_elements(By.CLASS_NAME,c.FILE_LINK_CLASS_NAME)
                if len(file_link_url_raw) > 0:
                    file_link_url = file_link_url_raw[0].get_attribute('href')
                    text_to_remove = li.find_element(By.CLASS_NAME,c.FILE_NAME_CHILD_TO_REMOVE_CLASS_NAME).text
                    file_moodle_name = li.find_element(By.CLASS_NAME,c.FILE_NAME_CLASS_NAME).text.replace(text_to_remove,"")

                    url_handler(self,file_link_url,file_moodle_name)
    
    def url_handler(self,url,file_name):
        # add logic 

        
if __name__ =='__main__':
    bw = Browser();
    bw.login()
    bw.course_dispatcher()
