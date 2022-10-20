from queue import Queue

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By


class Moder:
    def __init__(self) -> None:
        self.driver = Firefox()
        self.messages = Queue()
        
    def login_mshp(self):
        raise NotImplementedError

    def get_new_messages(self):
        buttons = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Одобрить')]").click()
        messages = self.driver.find_elements(By.CLASS_NAME, "ChatMessage__msgSequence___aT9Dk")
        for message in messages:
            self.messages.put(message)
        
