from selenium import webdriver
from selenium.webdriver.chrome.service import Service


options = webdriver.ChromeOptions()
options.add_argument("debuggerAddress localhost:2828")
driver = webdriver.Chrome(options=options)
# driver = webdriver.Firefox(service=Service("/usr/bin/firefox", service_args=['--connect-existing']))

driver.get("https://www.google.com")
pageSource = driver.page_source
print(pageSource)
