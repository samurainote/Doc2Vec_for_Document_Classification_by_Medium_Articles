
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome('/Users/akr712/Desktop/web scraping/chromedriver')
driver.get("https://byteacademy.co/")
assert "Python" in driver.title
elem = driver.find_element_by_neme("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(keys.RETURN)
