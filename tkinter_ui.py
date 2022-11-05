import tkinter as tk
from tkinter import Tk, Label, Text, Button
from selenium.webdriver.common.by import By


class TkinterUI:
    def __init__(self, web_plug):
        self.web_plug = web_plug
        self.window = Tk()

        self.question_label = Label(
            self.window, text="Question from ", font=("Helvetica 16 bold")
        )
        self.greeting_label = Label(
            self.window, text="greeting is:", font=("Helvetica 14")
        )
        self.answer_label = Label(
            self.window, text="Proposed answer", font=("Helvetica 16 bold")
        )
        self.text = Text(self.window, height=15, width=52)
        self.last_status_label = Label(
            self.window, text="Logging into the MSHP page", font=("Helvetica 10 italic")
        )

        self.b3 = Button(self.window, text="Exit", command=self.window.destroy)

        self.replies_box = tk.Listbox(self.window, width=60, height=20)
        for i in range(len(self.web_plug.relevant_responses)):
            self.replies_box.insert(i, self.web_plug.relevant_responses[i][1])

    def update_view(self):
        self.question_label.config(
            text=f"Question from {self.web_plug.student_full_name.strip()}"
        )
        self.greeting_label.config(
            text=f"greeting is: " + ("ON" if self.web_plug.greeting != "" else "OFF")
        )
        self.text.delete("1.0", tk.END)
        self.answer_label.config(
            text=self.web_plug.relevant_responses[self.web_plug.cur_response][0]
        )
        self.text.insert(
            tk.END, self.web_plug.relevant_responses[self.web_plug.cur_response][1]
        )
        self.last_status_label.config(text=self.web_plug.last_status)
        self.replies_box.delete(0, tk.END)
        for i in range(len(self.web_plug.relevant_responses)):
            self.replies_box.insert(i, self.web_plug.relevant_responses[i][1])

    def update_greeting(self):
        self.greeting_label.config(
            text=f"greeting is: " + ("ON" if self.web_plug.greeting != "" else "OFF")
        )

    def hook_update(self, target, hook, *args, **kwargs):
        target(*args, **kwargs)
        hook()

    def custom_answer(self):
        answer = self.text.get("1.0", tk.END)
        keywords = self.web_plug.question_text.split()
        self.web_plug.faq.update_faq({answer: list(set(keywords))})
        response = self.web_plug.greeting + answer
        self.web_plug.driver.find_element(
            By.CLASS_NAME, "auto-textarea-input"
        ).send_keys(response)

    def send_response(self):
        answer = self.text.get("1.0", tk.END)
        response = self.web_plug.greeting + answer
        self.web_plug.driver.find_element(
            By.CLASS_NAME, "auto-textarea-input"
        ).send_keys(response)

    def insert_codeblock(self):
        self.text.insert(tk.END, "\n```python\n\n```")
        cursor_position = self.text.index(tk.INSERT)
        x, _ = cursor_position.split(".")
        self.text.mark_set("insert", f"{int(x)-1}.{0}")

    def _bind_shortcuts(self):
        """Shortcuts are bound in this function"""

        mappings = [
            (
                lambda _: self.window.destroy(),
                "<Control-q>",
                "<Control-Cyrillic_shorti>",
            ),
            (
                lambda _: self.text.insert(tk.END, "`"),
                "<Control-k>",
                "<Control-Cyrillic_el>",
            ),
            (lambda _: self.insert_codeblock(), "<Control-j>", "<Control-Cyrillic_o>"),
            (
                lambda _: self.hook_update(
                    self.web_plug.refresh_questions, self.update_view
                ),
                "<Control-r>",
                "<Control-Cyrillic_ka>",
            ),
            (
                lambda _: self.hook_update(
                    self.web_plug.next_question, self.update_view
                ),
                "<Control-d>",
                "<Control-Cyrillic_ve>",
            ),
            (
                lambda _: self.hook_update(
                    self.web_plug.next_question, self.update_view, prev=True
                ),
                "<Control-u>",
                "<Control-Cyrillic_ghe>",
            ),
            (
                lambda _: self.web_plug.go_to_assignment(),
                "<Control-m>",
                "<Control-Cyrillic_softsign>",
            ),
            (
                lambda _: self.hook_update(
                    self.web_plug.toggle_greeting, self.update_greeting
                ),
                "<Control-g>",
                "<Control-Cyrillic_pe>",
            ),
            (
                lambda _: self.hook_update(
                    self.web_plug.next_response, self.update_view
                ),
                "<Control-n>",
                "<Control-Cyrillic_te>",
            ),
            (
                lambda _: self.hook_update(
                    self.web_plug.next_response, self.update_view, prev=True
                ),
                "<Control-p>",
                "<Control-Cyrillic_ze>",
            ),
            (lambda _: self.custom_answer(), "<Control-c>", "<Control-Cyrillic_es>"),
            (lambda _: self.send_response(), "<Control-i>", "<Control-Cyrillic_sha>"),
            (
                lambda _: self.hook_update(
                    self.web_plug.close_answer, self.update_view
                ),
                "<Control-z>",
                "<Control-Cyrillic_ya>",
            ),
            (
                lambda _: self.hook_update(self.web_plug.send_answer, self.update_view),
                "<Control-s>",
                "<Control-Cyrillic_yeru>",
            ),
            (
                lambda _: self.hook_update(
                    self.web_plug.send_and_close_answer, self.update_view
                ),
                "<Control-S>",
                "<Control-Cyrillic_YERU>",
            ),
            (
                lambda _: self.text.delete("1.0", tk.END),
                "<Control-a>",
                "<Control-Cyrillic_ef>",
            ),
        ]

        for m in mappings:
            self.window.bind(m[1], m[0])
            self.window.bind(m[2], m[0])

        self.replies_box.bind("<Double-Button>", lambda _: self.choose_reply())

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
