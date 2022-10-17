#!/usr/bin/python
from tui import TUI
from web_plug import WebPlug
from faq import FAQManager


def main():
    web_plug = WebPlug()
    tui = TUI(web_plug)
    tui.parse_input()


if __name__ == "__main__":
    main()
