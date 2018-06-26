from selenium import webdriver
import time

def start(url):
    driver = webdriver.Chrome('/home/zulbukharov/Загрузки/chromedriver')
    driver.get(url)
    driver.find_element_by_css_selector('div.link-phone').click()
    time.sleep(3)
    res = driver.find_element_by_css_selector('div.link-phone')
    return res.text
