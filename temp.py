from sys import dont_write_bytecode
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from secrets import USERNAME, PASSWORD

def main():
    driver = webdriver.Firefox()
    driver.get("https://md.hit.ac.il/")
    sleep(2)

    text = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/ul/li[1]/a").text
    print(text)

    # driver.refresh()

    if "https://md.hit.ac.il/" != driver.title:
        login(driver)
        # dfjsdf = ""
    

# def get_content(driver):
#     foler_name = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/section[2]/aside/section[1]/div/div/div[1]/div[1]/a").text
    

def refresh(driver):
    driver.refresh()
    driver.switch_to.alert.accept() # dismisses the alert of a refresh in login page
    sleep(2)
    if "https://is.hit.ac.il" in driver.current_url:
        print("need to login")
        login(driver)


def login(driver):
    print("Please log in")
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    # driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[1]/form/input[5]").click()
    sleep(2)


    # sleep(2)
    # if "https://md.hit.ac.il/" == driver.title:
    #     print("Logged in")
    # else:
    #     driver.close()
    #     sys.exit()


if __name__ =='__main__':
    main()