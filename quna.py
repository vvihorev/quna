#!/usr/bin/python
from web_plug import WebPlug
from tkinter_ui import TkinterUI
from faq import FAQManager


def main():
    web_plug = WebPlug()
    ui = TkinterUI(web_plug)
    web_plug.log_in_mshp()
    ui.run()


if __name__ == "__main__":
    main()
