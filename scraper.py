# from ast import Not
# from sys import dont_write_bytecode
# import sys
# from typing import List
import string
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options as FirefoxOptions

import config
import constants as c
from secrets import USERNAME, PASSWORD
from storage import Storage

class Browser:
    """Browser object that handles all the necessary functions
    """
    def __init__(self) -> None:
        """initialize the browser basic config options to download
        """
        my_firefox_options = webdriver.FirefoxOptions()

        # my_firefox_options = FirefoxOptions()
        my_firefox_options.set_preference("browser.download.folderList", 1)
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

        # self.driver = webdriver.Firefox(options=my_firefox_options)

        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            # command_executor='http://localhost:4444/session',
            options=my_firefox_options
        )
        self.storage = Storage()

    def login(self):
        """Go to login URL and log in the url \n
        *DOES NOT HANDLE REDIRECT*
        """
        self.driver.get(c.LOGIN_PAGE_URL)
        self.driver.find_element(By.ID, "username").send_keys(USERNAME)
        self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
        # Logic Button
        self.driver.find_element(By.XPATH, c.LOGIN_BUTTON).click()

        if self.driver.current_url != c.LOGIN_PAGE_URL:
            print("Logged in")
        else:
            print("login failed")
            self.driver.close()
            raise Exception("Login failed")

    def course_dispatcher(self) -> None:
        """ Scan the page for all the relevant courses and send them to be parsed
            assume logged in and redirected to home page
        """
        all_courses_div = self.driver.find_element(By.XPATH, c.ALL_COURSES_DIV_XPATH)
        courses = all_courses_div.find_elements(By.XPATH, c.COURSE_CLASS_NAME_XPATH)

        course_names = list()
        course_urls = list()

        for course in courses:
            course_name = self._remove_child_text(course, By.XPATH, c.COURSE_CHILD_TO_REMOVE_XPATH, course.text)
            if course_name in config.COURSES_TO_SCAN:
                course_url = course.find_element(By.TAG_NAME,"a").get_attribute('href')
                course_names.append(course_name)
                course_urls.append(course_url)
                # break

        for name,url in zip(course_names, course_urls):
            self.course_extractor(name,url)

        self.close_all()

    def course_extractor(self, course_name, course_url) -> None:
        """ extracting all crouse content

        Args:
            course_name (string): hebrew course name
            course_url (string): course url
        """
        self.storage.change_course(course_name)
        self.driver.get(course_url)

        sections = self.driver.find_elements(By.XPATH, c.DIV_SECTION_XPATH)
        print(f"{len(sections)=}")

        for section in sections:
            self._section_extractor(section)

    def _section_extractor(self, section) -> None:
        """ extract a section

        Args:
            section (WebElement): WebElement of a section
        """

        section_ul = section.find_elements(By.CLASS_NAME, c.UL_CLASS_NAME)
        if len(section_ul) > 0:
            section_name = section.find_element(By.TAG_NAME,"h3").text
            self.storage.change_section(section_name)
            self.summary_handler(section)
            sections_li = section_ul[0].find_elements(By.CLASS_NAME, c.LI_CLASS_NAME)

            for sec_li in sections_li:
                file_link_raw = sec_li.find_elements(By.CLASS_NAME,c.FILE_LINK_CLASS_NAME)

                # checking if this `li` contains a link - there some `li` with just text
                if len(file_link_raw) > 0:
                    self._link_handler(sec_li, file_link_raw)

    def summary_handler(self, section) -> None:
        """ creates a special row in database if there a summary
            section_name = section
            file_name = Summary
            url = ""
        Args:
            section (WebElement): current section
        """
        try:
            summary = section.find_element(By.CLASS_NAME, c.SECTION_SUMMARY_CLASS_NAME).text
            if summary != "":
            # change late
                self.storage.add_if_summary_is_new(summary)
        except:
            pass

    def _link_handler(self, contex, file_url):
        """ assume there is a link, extract all the relevant information

        Args:
            contex (WebElement): current context
            file_url (WebElement): WebElement containing the link
        """
        file_url = file_url[0].get_attribute('href')

        file_name_raw = contex.find_element(By.CLASS_NAME,c.FILE_NAME_CLASS_NAME).text
        file_name = self._remove_child_text(
            contex, By.CLASS_NAME, c.FILE_NAME_CHILD_CLASS_NAME, file_name_raw)

        extra_details = ""
        try:
            extra_details = contex.find_element(By.CLASS_NAME, c.EXTRA_DETAILS_CLASS_NAME).text
        except:
            pass

        is_new = self.storage.is_new_item(file_name, file_url)

        if is_new:
            # self.storage._add_new_entry(file_name, file_url, extra_details)
            self._url_handler(file_name, file_url, extra_details)

    def _url_handler(self, url, file_name, extra_detail) -> None:
        # add logic | folder -> file names in extra_details
        print("placeholder for _url_handler")

    @staticmethod
    def _remove_child_text(context, by_selector, child_selector, original_text) -> string:
        """remove child inner text from original string

        Args:
            context (WebElement): Webelement with the proper resolution
            by_selector (By.*SELECTOR): the type of By selector
            child_selector (string): selector of the child element to remove
            original_text (string): text to operatate on

        Returns:
            string: new string with the new name
        """
        text_to_remove = ""
        try:
            text_to_remove = context.find_element(by_selector, child_selector).text
        except:
            pass
        return str.strip(original_text.replace(text_to_remove, ""))

    def close_all(self):
        """ Close browser and database connection
        """
        # telegram bot, powerautomate
        self.storage.close_connection()
        self.driver.quit()




if __name__ =='__main__':
    bw = Browser()
    bw.login()
    try:
        bw.course_dispatcher()
    except:
        print("Failed")
        bw.close_all()
