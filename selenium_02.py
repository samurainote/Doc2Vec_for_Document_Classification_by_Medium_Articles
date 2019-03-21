from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome('/Users/akr712/Desktop/web scraping/chromedriver')
driver.get("https://www.amazon.in/Amazon-Brand-Solimo-Automatic-Umbrella/dp/B071DXFS9L/ref=sr_1_8?ie=UTF8&qid=1547808289&sr=8-8&keywords=umbrella")
assert "Python" in driver.title
elem = driver.find_element_by_class_name("twisterImageDiv twisterImageDivWrapper")

elem.clear()
elem.send_keys("")
elem.send_keys(keys.RETURN)
