import os
import time

from getch import getch


class TUI:
    def __init__(self, web_plug):
        self.web_plug = web_plug

    def main_page(self):
        os.system("clear")
        greeting_status = "OFF" if self.web_plug.greeting == "" else "ON"
        print("-------------------")
        print(f"Waiting for your action... [Greeting: {greeting_status}] [d/u/i]")
        print(f"Proposed answer: to {self.web_plug.student_name}")
        print("-------------------")
        print(self.web_plug.relevant_responses[self.web_plug.cur_response])
        print("-------------------")
        print("Last status: ", self.web_plug.last_status)

    def pend_questions(self):
        while True:
            try:
                print("Sleeping, waiting for questions")
                time.sleep(120)
            except KeyboardInterrupt:
                break
            print("Refreshing questions")
            self.web_plug.refresh_questions()
            if len(self.web_plug.questions) > 0:
                print("\a")
                return

    def run(self):
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
                case "P":
                    self.web_plug.pick_response()
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
                case "??":
                    self.web_plug.refresh_questions()
                case "??":
                    self.web_plug.next_question()
                case "??":
                    self.web_plug.next_question(prev=True)
                case "??":
                    self.web_plug.go_to_assignment()
                case "??":
                    self.web_plug.log_in_mshp()
                case "??":
                    self.web_plug.toggle_greeting()
                case "??":
                    self.web_plug.next_response()
                case "??":
                    self.web_plug.next_response(prev=True)
                case "??":
                    self.web_plug.pick_response()
                case "??":
                    self.web_plug.custom_answer()
                case "??":
                    self.web_plug.close_answer()
                case "??":
                    self.web_plug.input_answer()
                case "??":
                    self.web_plug.send_answer()
                case "??":
                    self.web_plug.send_and_close_answer()
                case "??":
                    quit()
                case "??":
                    self.pend_questions()
                case "??":
                    os.system("clear")
                case _:
                    print(input)
