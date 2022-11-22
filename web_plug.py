import os
import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import dotenv
import pyperclip

from faq import FAQManager


class WebPlug:
    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.driver = webdriver.Chrome()

        self.cur_question = 0
        self.questions = []

        self.student_name = ""
        self.student_full_name = ""
        self.greeting = ""
        self.question_text = "No question found/opened"

        self.faq = FAQManager("faq.json")
        self.relevant_responses = [""]
        self.cur_response = 0

        self.last_status = "Hello!"

    def wait_for_element(self, by, query):
        """Waits until the page element is loaded, unless timeout happens"""
        timeout = 7
        try:
            element_present = expected_conditions.presence_of_element_located(
                (by, query)
            )
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            self.last_status = "Timed out waiting for page to load"

    def get_question_info(self):
        if len(self.questions) == 0:
            self.student_name = ""
            self.student_full_name = ""
            self.question_text = "No questions found"
        else:
            try:
                self.student_name = self.questions[self.cur_question].text.split()[-1]
                self.student_full_name = re.sub(
                    r"\d", "", self.questions[self.cur_question].text
                )
            except:
                self.last_status = "Имя студента не нашлось :("
            self.question_text = self.get_question_header()
        pyperclip.copy(self.student_full_name)
        self.greeting = f"Добрый день, {self.student_name} :)\n"
        self.relevant_responses = self.faq.get_responses(self.question_text)
        self.cur_response = 0

    def log_in_mshp(self) -> None:
        """Log in to the mshp.ru website and open the questions tab."""
        self.last_status = "Logging into the mshp page"
        try:
            self.driver.get("https://my.mshp.ru/accounts/login/#/")
        except:
            print("No internet connection, sorry :(")
            input()
            exit()
        login_button = self.driver.find_element(By.LINK_TEXT, "Вход для сотрудников")
        login_button.click()
        self.driver.find_element(By.ID, "username").send_keys(os.environ["USERNAME"])
        self.driver.find_element(By.ID, "password").send_keys(os.environ["PASSWORD"])
        self.driver.find_element(By.XPATH, "//*[contains(text(), 'Войти')]").click()

        # self.wait_for_element(By.XPATH, "//*[contains(text(), 'Вопросы')]")
        # self.driver.find_element(By.XPATH, "//*[contains(text(), 'Вопросы')]").click()
        # try:
        # self.wait_for_element(By.CLASS_NAME, "discus-row")
        # self.driver.find_element(By.CLASS_NAME, "discus-row").click()
        # except:
        # self.last_status = "No questions found, refresh later"
        # return
        # self.refresh_questions()

    def refresh_questions(self) -> None:
        self.driver.refresh()
        self.wait_for_element(By.CLASS_NAME, "discus-row")
        self.questions = self.driver.find_elements(By.CLASS_NAME, "discus-row")
        self.last_status = f"Found {len(self.questions)} questions"
        self.cur_question = 0
        if len(self.questions) > 0:
            self.questions[self.cur_question].click()
            self.get_question_info()

    def next_question(self, prev=False) -> None:
        """Click on the next question in list."""
        which = "prev" if prev else "next"
        if self.questions == []:
            self.last_status = "No questions found, refreshing"
            self.refresh_questions()
            return
        self.last_status = f"Going to the {which} question"
        if prev:
            if self.cur_question >= 1:
                self.cur_question -= 1
            else:
                return
        elif self.cur_question < len(self.questions) - 1:
            self.cur_question += 1
        else:
            return
        try:
            self.questions[self.cur_question].click()
        except:
            self.refresh_questions()
            return
        self.get_question_info()

    def next_response(self, prev=False) -> None:
        if len(self.relevant_responses) <= 1:
            self.last_status = "No relevant responses found"
            return
        which = "prev" if prev else "next"
        self.last_status = f"Going to the {which} response"
        if prev:
            if self.cur_response >= 1:
                self.cur_response -= 1
            else:
                self.last_status = "No more responses found"
        elif self.cur_response < len(self.relevant_responses) - 1:
            self.cur_response += 1
        else:
            self.last_status = "No more responses found"

    def get_question_header(self) -> str:
        """Get text of the last message in the current question."""
        self.wait_for_element(
            By.XPATH, "//div[contains(@class, 'comment_message__text')]"
        )
        question_header = self.driver.find_element(By.CLASS_NAME, "h4").text
        return question_header

    def send_and_close_answer(self) -> None:
        """Find and press the 'send and close answer' button."""
        self.last_status = "Sending the answer and closing the discussion"
        self.driver.find_element(
            By.XPATH, "//*[contains(text(), 'Отправить и закрыть')]"
        ).click()

    def send_answer(self) -> None:
        """Find and press the 'send answer' button."""
        self.last_status = "Sending the answer..."
        self.driver.find_element(By.XPATH, "//*[contains(text(), 'Отправить')]").click()

    def close_answer(self) -> None:
        """Closes the current discussion"""
        self.driver.find_element(
            By.XPATH, "//*[contains(text(), 'Закрыть вопрос')]"
        ).click()

    def toggle_greeting(self) -> None:
        if self.greeting == "":
            self.greeting = f"Добрый день, {self.student_name} :)\n"
            print("Greeting set to ON")
        else:
            self.greeting = ""
            print("Greeting set to OFF")

    def go_to_assignment(self) -> None:
        self.last_status = "Going to the assignment"
        self.driver.find_element(By.CLASS_NAME, "icon-link").click()
