# Quna

This is a TUI helper for chat support workers.

## Quna main features

- custom terminal UI
- vim-like hotkeys for responses, problem inspection, etc.
- greeting toggle for responses
- proposition of likely responses from FAQ
- sleep mode, quna will check for new messages every two minutes
- menu to pick response from the FAQ list

## Brief module description

- tui - Custom terminal UI
  - getch - Get a single character from stdin, used in tui
- faq - Manage faq.json and provide response recommendations
- web_plug - Connect to the browser
- quna - Entry point

## TODO:

- make interface asynchronous
- ability to connect to a running browser session

### ChatModerator bot

- search for "ОДОБРИТЬ" buttons, display messages that contain these buttons
- add hotkeys to approve or skip the message in question
- display message in a separate program window, so the chat does not have to be scrolled
- sound notification about new messages if no messages have appeared in the last 2 seconds
