import os
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from helpers.scraper.scraper_constants import *


def selenium_driver_init():
    dirname = os.path.dirname(__file__)
    relative_path_to_chrome_linux_driver = "./selenium_webdriver/linux64chromedriver"
    absolute_path_to_chrome_linux_driver = os.path.join(
        dirname, relative_path_to_chrome_linux_driver)

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(
        executable_path=absolute_path_to_chrome_linux_driver, options=options)

    return driver


def check_exists_by_xpath(selenium_web_driver, xpath):
    try:
        selenium_web_driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def is_valid_post(selenium_web_driver):
    if check_exists_by_xpath(selenium_web_driver, XPATH_FOR_TWEET_NOT_FOUND):
        return False
    return True


def get_tweet_post_text(selenium_web_driver):
    tweet_text = selenium_web_driver.find_element_by_css_selector(
        CSS_SELECTOR_FOR_TWEET_TEXT)
    return tweet_text.text


def get_tweet_post_replies(selenium_web_driver):

    replies = set()
    while True:
        if check_exists_by_xpath(selenium_web_driver, XPATH_FOR_SHOW_MORE_REPLIES_BUTTON):
            show_more_element = selenium_web_driver.find_element_by_xpath(
                XPATH_FOR_SHOW_MORE_REPLIES_BUTTON)
            selenium_web_driver.execute_script(
                "arguments[0].click();", show_more_element)
            time.sleep(4)

        for reply in selenium_web_driver.find_elements_by_xpath(XPATH_FOR_TWEET_REPLY):
            replies.add(reply.text)

        last_height = selenium_web_driver.execute_script(
            "return document.body.scrollHeight")
        selenium_web_driver.execute_script(
            f"window.scrollTo(0, {last_height})")
        time.sleep(2)
        new_height = selenium_web_driver.execute_script(
            "return document.body.scrollHeight")

        if last_height == new_height:
            break

    return replies


def fetch_post_text(url):

    selenium_web_driver = selenium_driver_init()
    selenium_web_driver.get(url)
    time.sleep(3)

    if not is_valid_post(selenium_web_driver):
        return {'post_found': False, 'error': 'post not found!'}

    tweet_text = get_tweet_post_text(selenium_web_driver)
    selenium_web_driver.quit()

    return {'post_found': True, 'tweet_text': tweet_text}


def fetch_post_replies(url):

    selenium_web_driver = selenium_driver_init()
    selenium_web_driver.get(url)
    time.sleep(3)

    if not is_valid_post(selenium_web_driver):
        return {'post_found': False, 'error': 'post not found!'}

    tweet_replies = get_tweet_post_replies(selenium_web_driver)
    selenium_web_driver.quit()

    return {'post_found': True, 'tweet_replies': tweet_replies}
