import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import dotenv
from rich.panel import Panel
from textual import events
from textual.app import App
from textual.widget import Widget
from textual.widgets import Header, Footer, ScrollView


dotenv.load_dotenv()
driver = webdriver.Firefox()

# TODO: add "Добрый день, {student_name} :)" to all messages
# TODO: automate opening of students solution to the problem in question
# TODO: match question with possible answers by keywords in question text, propose options
# TODO: notify about new questions, refresh page every 5 minutes
# TODO: add hotkeys interface to perform all the actions


cur_question = 0
questions = []


def log_in_mshp() -> None:
    """Log in to the mshp.ru website and open the questions tab."""
    driver.get("https://my.mshp.ru/accounts/login/#/")
    login_button = driver.find_element(By.LINK_TEXT, "Вход для сотрудников")
    login_button.click()
    driver.find_element(By.ID, "username").send_keys(os.environ["USERNAME"])
    driver.find_element(By.ID, "password").send_keys(os.environ["PASSWORD"])
    driver.find_element(By.XPATH, "//*[contains(text(), 'Войти')]").click()
    driver.find_element(By.XPATH, "//*[contains(text(), 'Вопросы')]").click()

def refresh_questions() -> None:
    driver.refresh()
    questions = driver.find_elements(By.CLASS_NAME, "discus-row")

def next_question() -> None:
    """Click on the next question in list."""
    cur_question += 1
    if questions == []:
        refresh_questions()
    questions[cur_question].click()

def prev_question() -> None:
    """Click on the next question in list."""
    if cur_question >= 1:
        cur_question -= 1
    if questions == []:
        refresh_questions()
    questions[cur_question].click()

def get_last_message_text() -> str:
    """Get text of the last message in the current question."""
    messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'comment_message__text')]")
    last_message_text = messages[-1].text
    if len(messages) > 1:
        last_message_text += messages[-2].text
    return last_message_text

async def input_answer(answer: str) -> None:
    """Inputs the given answer into the textarea."""
    driver.find_element(By.CLASS_NAME, "auto-textarea-input").send_keys(answer)

def send_and_close_answer() -> None:
    """Find and press the 'send and close answer' button."""
    driver.find_element(By.XPATH, "//*[contains(text(), 'Отправить и закрыть')]").click()

def send_answer() -> None:
    """Find and press the 'send answer' button."""
    driver.find_element(By.XPATH, "//*[contains(text(), 'Отправить')]").click()

def accept_response() -> None:
    raise NotImplementedError

def toggle_greeting() -> None:
    raise NotImplementedError

input()
