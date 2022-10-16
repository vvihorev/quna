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
# driver = webdriver.Firefox()

# TODO: add "Добрый день, {student_name} :)" to all messages
# TODO: automate opening of students solution to the problem in question
# TODO: match question with possible answers by keywords in question text, propose options
# TODO: notify about new questions, refresh page every 5 minutes
# TODO: add hotkeys interface to perform all the actions


class Quna(App):
    """An example of a very simple Textual App"""
    def __init__(self, *args, **kwargs):
        super(Quna, self).__init__(*args, **kwargs)
        self.cur_question = 0
        self.questions = []

    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("R", "refresh_questions", "Refresh")
        await self.bind("d", "next_question", "Next Question")
        await self.bind("u", "prev_question", "Prev Question")
        await self.bind("O", "log_in_mshp", "Login")
        await self.bind("g", "toggle_greeting", "Toggle Greeting")
        await self.bind("enter", "accept_suggestion", "Accept Response")
        await self.bind("n", "next_response", "Next Response")
        await self.bind("p", "prev_response", "Prev Response")
        await self.bind("c", "custom_answer", "Custom Answer")
        await self.bind("i", "modify_answer", "Modify Answer")
        await self.bind("s", "send", "Send")
        await self.bind("S", "send_and_close", "Send & Close")
        await self.bind("q", "quit", "Quit")
        await self.bind("escape", "quit", "Quit")

    async def action_update_body(self):
        await self.body.update("\nHello, world!")

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
        if self.questions == []:
            await self.action_refresh_questions()
        self.questions[self.cur_question].click()

    async def action_prev_question(self) -> None:
        """Click on the next question in list."""
        if self.cur_question >= 1:
            self.cur_question -= 1
        if self.questions == []:
            await self.action_refresh_questions()
        self.questions[self.cur_question].click()

    async def action_get_last_message_text(self) -> str:
        """Get text of the last message in the current question."""
        messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'comment_message__text')]")
        last_message_text = messages[-1].text
        if len(messages) > 1:
            last_message_text += messages[-2].text
        return last_message_text

    async def input_answer(self, answer: str) -> None:
        """Inputs the given answer into the textarea."""
        driver.find_element(By.CLASS_NAME, "auto-textarea-input").send_keys(answer)

    async def action_send_and_close_answer(self) -> None:
        """Find and press the 'send and close answer' button."""
        driver.find_element(By.XPATH, "//*[contains(text(), 'Отправить и закрыть')]").click()

    async def action_send_answer(self) -> None:
        """Find and press the 'send answer' button."""
        driver.find_element(By.XPATH, "//*[contains(text(), 'Отправить')]").click()

    async def action_accept_response(self) -> None:
        raise NotImplementedError

    async def action_toggle_greeting(self) -> None:
        raise NotImplementedError

    async def on_mount(self, event: events.Mount) -> None:
        """Create and dock the widgets."""
        self.body = ScrollView(gutter=1)
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(self.body, edge="left", size=50)


Quna.run(title="Quna", log="app.log")
