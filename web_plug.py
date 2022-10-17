import os
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import dotenv

from faq import FAQManager


class WebPlug:
    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.driver = webdriver.Firefox()

        self.cur_question = 0
        self.questions = []

        self.student_name = ""
        self.greeting = ""
        self.question_text = "No question found/opened"

        self.faq = FAQManager("faq.json")
        self.relevant_responses = [""]
        self.cur_response = 0

        self.last_status = "Hello!"

    def wait_for_element(self, by, query):
        timeout = 7
        try:
            element_present = expected_conditions.presence_of_element_located(
                (by, query)
            )
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            self.last_status = "Timed out waiting for page to load"

    def get_question_info(self):
        self.student_name = self.questions[self.cur_question].text.split()[-1]
        self.greeting = f"Добрый день, {self.student_name} :)\n"
        self.question_text = self.get_last_message_text()
        self.relevant_responses = self.faq.get_responses(self.question_text)

    def log_in_mshp(self) -> None:
        """Log in to the mshp.ru website and open the questions tab."""
        print("Logging into the mshp page")
        self.last_status = "Logging into the mshp page"
        self.driver.get("https://my.mshp.ru/accounts/login/#/")
        login_button = self.driver.find_element(By.LINK_TEXT, "Вход для сотрудников")
        login_button.click()
        self.driver.find_element(By.ID, "username").send_keys(os.environ["USERNAME"])
        self.driver.find_element(By.ID, "password").send_keys(os.environ["PASSWORD"])
        self.driver.find_element(By.XPATH, "//*[contains(text(), 'Войти')]").click()

        self.wait_for_element(By.XPATH, "//*[contains(text(), 'Вопросы')]")
        self.driver.find_element(By.XPATH, "//*[contains(text(), 'Вопросы')]").click()
        self.wait_for_element(By.CLASS_NAME, "discus-row")
        self.driver.find_element(By.CLASS_NAME, "discus-row").click()
        self.refresh_questions()

    def refresh_questions(self) -> None:
        print("Refreshing questions")
        self.last_status = "Refreshing questions"
        self.driver.refresh()
        self.wait_for_element(By.CLASS_NAME, "discus-row")
        time.sleep(2)
        self.questions = self.driver.find_elements(By.CLASS_NAME, "discus-row")
        print(f"Found {len(self.questions)} questions")
        self.last_status = f"Found {len(self.questions)} questions"
        self.get_question_info()

    def next_question(self, prev=False) -> None:
        """Click on the next question in list."""
        which = "prev" if prev else "next"
        if self.questions == []:
            print("No questions found, refreshing")
            self.last_status = "No questions found, refreshing"
            self.refresh_questions()
        print(f"Going to the {which} question")
        self.last_status = f"Going to the {which} question"
        if prev and self.cur_question >= 1:
            self.cur_question -= 1
        elif self.cur_question < len(self.questions) - 1:
            self.cur_question += 1
        else:
            print("No more questions found")
            return
        self.questions[self.cur_question].click()
        self.get_question_info()

    def next_response(self, prev=False) -> None:
        if len(self.relevant_responses) <= 1:
            print("No relevant responses found")
            self.last_status = "No relevant responses found"
            return
        which = "prev" if prev else "next"
        print(f"Going to the {which} response")
        self.last_status = f"Going to the {which} response"
        if prev and self.cur_response >= 1:
            self.cur_response -= 1
        elif self.cur_response < len(self.relevant_responses) - 1:
            self.cur_response += 1
        else:
            print("No more responses found")
            self.last_status = "No more responses found"

    def get_last_message_text(self) -> str:
        """Get text of the last message in the current question."""
        self.wait_for_element(
            By.XPATH, "//div[contains(@class, 'comment_message__text')]"
        )
        messages = self.driver.find_elements(
            By.XPATH, "//div[contains(@class, 'comment_message__text')]"
        )
        last_message_text = "Message was not found"
        if len(messages) > 0:
            last_message_text = messages[-1].text
        elif len(messages) > 1:
            last_message_text = messages[-2].text + "\n" + last_message_text
        return last_message_text

    def input_answer(self) -> None:
        """Inputs the given answer into the textarea."""
        os.system("clear")
        print("The question is:")
        print(self.question_text)
        print("-------------------")
        print("Input your answer: (input '' to exit)")
        print(self.greeting)
        input_answer = input()
        if input_answer == "":
            os.system("clear")
            print("Quitting from edit mode")
            self.last_status = "Quitting from edit mode"
            return
        answer = self.greeting + input_answer
        self.driver.find_element(By.CLASS_NAME, "auto-textarea-input").send_keys(answer)

    def custom_answer(self) -> None:
        """Adds a new answer to the FAQ"""
        print("Adding custom answer to the FAQ")
        print("Write down your answer: ('' to exit)")
        answer = input()
        if answer == "":
            return
        print("Write down some keywords: ('' to exit)")
        input_keywords = input()
        if input_keywords != "":
            keywords = input_keywords.split()
            self.faq.update_faq({answer: keywords})
        self.driver.find_element(By.CLASS_NAME, "auto-textarea-input").send_keys(answer)

    def send_and_close_answer(self) -> None:
        """Find and press the 'send and close answer' button."""
        print("Sending the answer and closing the discussion")
        self.last_status = "Sending the answer and closing the discussion"
        self.driver.find_element(
            By.XPATH, "//*[contains(text(), 'Отправить и закрыть')]"
        ).click()

    def send_answer(self) -> None:
        """Find and press the 'send answer' button."""
        print("Sending the answer...")
        self.last_status = "Sending the answer..."
        self.driver.find_element(By.XPATH, "//*[contains(text(), 'Отправить')]").click()

    def toggle_greeting(self) -> None:
        if self.greeting == "":
            self.greeting = f"Добрый день, {self.student_name} :)\n"
            print("Greeting set to ON")
        else:
            self.greeting = ""
            print("Greeting set to OFF")

    def go_to_assignment(self) -> None:
        print("Going to the assignment")
        self.last_status = "Going to the assignment"
        self.driver.find_element(By.CLASS_NAME, "icon-link").click()
