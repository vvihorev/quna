from selenium import webdriver
from selenium.webdriver.firefox.service import Service


driver = webdriver.Firefox(service=Service("/usr/bin/firefox", service_args=['--marionette-port', '2828', '--connect-existing']))

driver.get("https://google.com")
pageSource = driver.page_source
print(pageSource)
