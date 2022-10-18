from selenium import webdriver
from selenium.webdriver.firefox.service import Service


driver = webdriver.Firefox(service=Service("/usr/bin/geckodriver", service_args=['--marionette-port', '2828', '--connect-existing']))

driver.get("https://www.google.com")
pageSource = driver.page_source
print(pageSource)
