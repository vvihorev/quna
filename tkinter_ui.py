import tkinter as tk
from tkinter import Tk, Label, Text, Button
from selenium.webdriver.common.by import By


class TkinterUI:
    def __init__(self, web_plug):
        self.web_plug = web_plug
        self.window = Tk()

        self.question_label = Label(self.window, text="Question from ", font=('Helvetica 16 bold'))
        self.greeting_label = Label(self.window, text="greeting is:", font=('Helvetica 14'))
        self.answer_label = Label(self.window, text="Proposed answer", font=('Helvetica 16 bold'))
        self.text = Text(self.window, height=15, width=52)
        self.last_status_label = Label(self.window, text="Logging into the MSHP page", font=('Helvetica 10 italic'))

        self.b3 = Button(self.window, text="Exit", command=self.window.destroy)

        self.replies_box = tk.Listbox(self.window, width=60)
        for i in range(len(self.web_plug.relevant_responses)):
            self.replies_box.insert(i, self.web_plug.relevant_responses[i][1])

    def update_view(self):
        self.question_label.config(text=f"Question from {self.web_plug.student_full_name.strip()}")
        self.greeting_label.config(text=f"greeting is: " + ("ON" if self.web_plug.greeting != "" else "OFF"))
        self.text.delete("1.0", tk.END)
        self.answer_label.config(text=self.web_plug.relevant_responses[self.web_plug.cur_response][0])
        self.text.insert(tk.END, self.web_plug.relevant_responses[self.web_plug.cur_response][1])
        self.last_status_label.config(text=self.web_plug.last_status)
        for i in range(len(self.web_plug.relevant_responses)):
            self.replies_box.insert(i, self.web_plug.relevant_responses[i][1])

    def hook_update(self, func, *args, **kwargs):
        func(*args, **kwargs)
        self.update_view()

    def custom_answer(self):
        answer = self.text.get("1.0", tk.END)
        keywords = self.web_plug.question_text.split()
        self.web_plug.faq.update_faq({answer: list(set(keywords))})
        response = self.web_plug.greeting + answer
        self.web_plug.driver.find_element(By.CLASS_NAME, "auto-textarea-input").send_keys(response)

    def send_response(self):
        answer = self.text.get("1.0", tk.END)
        response = self.web_plug.greeting + answer
        self.web_plug.driver.find_element(By.CLASS_NAME, "auto-textarea-input").send_keys(response)

    def _bind_shortcuts(self):
        """Shortcuts are bound in this function"""
        self.window.bind('<Control-q>', lambda _: self.window.destroy())
        self.window.bind('<Control-k>', lambda _: self.text.insert(tk.END, "`"))
        self.window.bind('<Control-j>', lambda _: self.text.insert(tk.END, "\n```python\n\n```"))
        self.window.bind('<Control-r>', lambda _: self.hook_update(self.web_plug.refresh_questions))
        self.window.bind('<Control-d>', lambda _: self.hook_update(self.web_plug.next_question))
        self.window.bind('<Control-u>', lambda _: self.hook_update(self.web_plug.next_question, prev=True))
        self.window.bind('<Control-m>', lambda _: self.hook_update(self.web_plug.go_to_assignment))
        self.window.bind('<Control-g>', lambda _: self.hook_update(self.web_plug.toggle_greeting))
        self.window.bind('<Control-n>', lambda _: self.hook_update(self.web_plug.next_response))
        self.window.bind('<Control-p>', lambda _: self.hook_update(self.web_plug.next_response, prev=True))
        # TODO: implement pick responses functionality
        # self.window.bind('<Control-l>', lambda _: self.hook_update(self.web_plug.pick_response))
        self.window.bind('<Control-c>', lambda _: self.custom_answer())
        self.window.bind('<Control-i>', lambda _: self.send_response())
        self.window.bind('<Control-z>', lambda _: self.hook_update(self.web_plug.close_answer))
        self.window.bind('<Control-s>', lambda _: self.hook_update(self.web_plug.send_answer))
        self.window.bind('<Control-S>', lambda _: self.hook_update(self.web_plug.send_and_close_answer))
        self.window.bind('<Control-a>', lambda _: self.text.delete("1.0", tk.END))

        self.window.bind('<Control-Cyrillic_shorti>', lambda _: self.window.destroy())
        self.window.bind('<Control-Cyrillic_el>', lambda _: self.text.insert(tk.END, "`"))
        self.window.bind('<Control-Cyrillic_o>', lambda _: self.text.insert(tk.END, "\n```python\n\n```"))
        self.window.bind('<Control-Cyrillic_ka>', lambda _: self.hook_update(self.web_plug.refresh_questions))
        self.window.bind('<Control-Cyrillic_ve>', lambda _: self.hook_update(self.web_plug.next_question))
        self.window.bind('<Control-Cyrillic_ghe>', lambda _: self.hook_update(self.web_plug.next_question, prev=True))
        self.window.bind('<Control-Cyrillic_softsign>', lambda _: self.hook_update(self.web_plug.go_to_assignment))
        self.window.bind('<Control-Cyrillic_pe>', lambda _: self.hook_update(self.web_plug.toggle_greeting))
        self.window.bind('<Control-Cyrillic_te>', lambda _: self.hook_update(self.web_plug.next_response))
        self.window.bind('<Control-Cyrillic_ze>', lambda _: self.hook_update(self.web_plug.next_response, prev=True))
        # TODO: implement pick responses functionality
        # self.window.bind('<Control-Cyrillic_>', lambda _: self.hook_update(self.web_plug.pick_response))
        self.window.bind('<Control-Cyrillic_es>', lambda _: self.custom_answer())
        self.window.bind('<Control-Cyrillic_sha>', lambda _: self.send_response())
        self.window.bind('<Control-Cyrillic_ya>', lambda _: self.hook_update(self.web_plug.close_answer))
        self.window.bind('<Control-Cyrillic_yeru>', lambda _: self.hook_update(self.web_plug.send_answer))
        self.window.bind('<Control-Cyrillic_YERU>', lambda _: self.hook_update(self.web_plug.send_and_close_answer))
        self.window.bind('<Control-Cyrillic_ef>', lambda _: self.text.delete("1.0", tk.END))

        self.replies_box.bind('<Double-Button>', lambda _: self.choose_reply())

    def choose_reply(self):
        reply = self.replies_box.get(self.replies_box.curselection())
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", reply)

    def _pack_ui_elements(self):
        """Location of interface elements is defined in this function"""
        self.question_label.pack()
        self.greeting_label.pack()
        self.last_status_label.pack(side=tk.BOTTOM)
        self.replies_box.pack()
        self.answer_label.pack()
        self.text.pack()
        self.b3.pack(side=tk.LEFT)

    def run(self):
        self._bind_shortcuts()
        self._pack_ui_elements()
        self.window.mainloop()
 
