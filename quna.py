import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import dotenv

from textual import events
from textual.app import App
from textual.widgets import Header, Footer, Placeholder, ScrollView


dotenv.load_dotenv()
driver = webdriver.Firefox()

# TODO: add "Добрый день, {student_name} :)" to all messages
# TODO: automate opening of students solution to the problem in question
# TODO: match question with possible answers by keywords in question text, propose options
# TODO: notify about new questions, refresh page every 5 minutes
# TODO: add hotkeys interface to perform all the actions


class MyApp(App):
    """An example of a very simple Textual App"""
    def __init__(self):
        self.cur_question = 0
        self.questions = []

    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("b", "view.toggle('sidebar')", "Toggle sidebar")
        await self.bind("q", "quit", "Quit")
        await self.bind("escape", "quit", "Quit")

    async def action_log_in_mshp(self) -> None:
        """Log in to the mshp.ru website and open the questions tab."""
        driver.get("https://my.mshp.ru/accounts/login/#/")
        login_button = driver.find_element(By.LINK_TEXT, "Вход для сотрудников")
        login_button.click()
        driver.find_element(By.ID, "username").send_keys(os.environ["USERNAME"])
        driver.find_element(By.ID, "password").send_keys(os.environ["PASSWORD"])
        driver.find_element(By.XPATH, "//*[contains(text(), 'Войти')]").click()
        driver.find_element(By.XPATH, "//*[contains(text(), 'Вопросы')]").click()

    async def action_refresh_questions(self) -> None:
        driver.refresh()
        self.questions = driver.find_elements(By.CLASS_NAME, "discus-row")

    async def action_next_question(self) -> None:
        """Click on the next question in list."""
        self.cur_question += 1
        self.questions[self.cur_question].click()

    async def action_get_last_message_text(self) -> str:
        """Get text of the last message in the current question."""
        messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'comment_message__text')]")
        last_message_text = messages[-1].text
        if len(messages) > 1:
            last_message_text += messages[-2].text
        return last_message_text

    async def action_input_answer(self, answer: str) -> None:
        """Inputs the given answer into the textarea."""
        driver.find_element(By.CLASS_NAME, "auto-textarea-input").send_keys(answer)

    async def action_send_and_close_answer(self) -> None:
        """Find and press the 'send and close answer' button."""
        driver.find_element(By.XPATH, "//*[contains(text(), 'Отправить и закрыть')]").click()

    async def action_send_answer(self) -> None:
        """Find and press the 'send answer' button."""
        driver.find_element(By.XPATH, "//*[contains(text(), 'Отправить')]").click()

    async def on_mount(self, event: events.Mount) -> None:
        """Create and dock the widgets."""
        # A scrollview to contain the markdown file
        body = ScrollView(gutter=1)
        # Header / footer / dock
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(Placeholder(), edge="left", size=30, name="sidebar")
        # Dock the body in the remaining space
        await self.view.dock(body, edge="right")


MyApp.run(title="Simple App")
