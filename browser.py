
from selenium import webdriver
import time

import config


def login(driver):
    driver.get("https://www.linkedin.com/")
    assert "LinkedIn" in driver.title

    email = driver.find_element_by_class_name("login-email")
    email.clear()
    email.send_keys(config.email)

    password = driver.find_element_by_class_name("login-password")
    password.clear()
    password.send_keys(config.password)

    submit = driver.find_element_by_class_name("submit-button")
    submit.click()


def get_browser():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    driver = webdriver.Chrome(chrome_options=options)
    return driver


def get_links(driver):
    elems = driver.find_elements_by_xpath("//a[@href]")
    links = []
    for elem in elems:
        links.append(elem.get_attribute("href"))

    return links


def scroll_to_bottom(driver):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return driver


def scroll_to_top(driver):
    driver.execute_script("window.scrollTo(0, 0);")

    return driver

