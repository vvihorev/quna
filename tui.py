import os

from getch import getch


class TUI:
    def __init__(self, web_plug):
        self.web_plug = web_plug

    def parse_input(self):
        while True:
            os.system("clear")
            greeting_status = "OFF" if self.web_plug.greeting == "" else "ON"
            print("The question is:")
            print(self.web_plug.question_text)
            print("-------------------")
            print(f"Waiting for your action... [Greeting: {greeting_status}] [d/u/i]")
            input = getch()
            match input:
                case "R": self.web_plug.refresh_questions()
                case "d": self.web_plug.next_question()
                case "u": self.web_plug.next_question(prev=True)
                case "m": self.web_plug.go_to_assignment()
                case "O": self.web_plug.log_in_mshp()
                case "g": self.web_plug.toggle_greeting()
                case "n": self.web_plug.next_response()
                case "p": self.web_plug.prev_response()
                case "c": self.web_plug.custom_answer()
                case "i": self.web_plug.input_answer()
                case "s": self.web_plug.send()
                case "S": self.web_plug.send_and_close()
                case "q": quit()
                case "l": os.system("clear")
                case "К": self.web_plug.refresh_questions()
                case "в": self.web_plug.next_question()
                case "г": self.web_plug.next_question(prev=True)
                case "ь": self.web_plug.go_to_assignment()
                case "Щ": self.web_plug.log_in_mshp()
                case "п": self.web_plug.toggle_greeting()
                case "т": self.web_plug.next_response()
                case "з": self.web_plug.prev_response()
                case "с": self.web_plug.custom_answer()
                case "ш": self.web_plug.input_answer()
                case "ы": self.web_plug.send()
                case "Ы": self.web_plug.send_and_close()
                case "й": quit()
                case "д": os.system("clear")
                case _: print(input)

