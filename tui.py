import os
import time

from getch import getch


class TUI:
    def __init__(self, web_plug):
        self.web_plug = web_plug

    def main_page(self):
        os.system("clear")
        greeting_status = "OFF" if self.web_plug.greeting == "" else "ON"
        print("The question is:")
        print("-------------------")
        print(self.web_plug.question_text)
        print("-------------------")
        print(f"Waiting for your action... [Greeting: {greeting_status}] [d/u/i]")
        print("Proposed answer:")
        print("-------------------")
        print(self.web_plug.relevant_responses[self.web_plug.cur_response])
        print("-------------------")
        print("Last status: ", self.web_plug.last_status)

    def pend_questions(self):
        while True:
            try:
                print("Sleeping, waiting for questions")
                time.sleep(300)
            except KeyboardInterrupt:
                break
            print("Refreshing questions")
            self.web_plug.refresh_questions()
            if len(self.web_plug.questions) > 0:
                print('\a')
                return

    def parse_input(self):
        while True:
            self.main_page()
            input = getch()
            match input:
                case "R":
                    self.web_plug.refresh_questions()
                case "d":
                    self.web_plug.next_question()
                case "u":
                    self.web_plug.next_question(prev=True)
                case "m":
                    self.web_plug.go_to_assignment()
                case "O":
                    self.web_plug.log_in_mshp()
                case "g":
                    self.web_plug.toggle_greeting()
                case "n":
                    self.web_plug.next_response()
                case "p":
                    self.web_plug.next_response(prev=True)
                case "c":
                    self.web_plug.custom_answer()
                case "i":
                    self.web_plug.input_answer()
                case "z":
                    self.web_plug.close_answer()
                case "s":
                    self.web_plug.send_answer()
                case "S":
                    self.web_plug.send_and_close_answer()
                case "q":
                    quit()
                case "w":
                    self.pend_questions()
                case "l":
                    os.system("clear")
                case "К":
                    self.web_plug.refresh_questions()
                case "в":
                    self.web_plug.next_question()
                case "г":
                    self.web_plug.next_question(prev=True)
                case "ь":
                    self.web_plug.go_to_assignment()
                case "Щ":
                    self.web_plug.log_in_mshp()
                case "п":
                    self.web_plug.toggle_greeting()
                case "т":
                    self.web_plug.next_response()
                case "з":
                    self.web_plug.next_response(prev=True)
                case "с":
                    self.web_plug.custom_answer()
                case "я":
                    self.web_plug.close_answer()
                case "ш":
                    self.web_plug.input_answer()
                case "ы":
                    self.web_plug.send_answer()
                case "Ы":
                    self.web_plug.send_and_close_answer()
                case "й":
                    quit()
                case "ц":
                    self.pend_questions()
                case "д":
                    os.system("clear")
                case _:
                    print(input)
