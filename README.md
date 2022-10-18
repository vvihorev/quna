# Quna

This is a TUI helper for chat support workers.

## Quna main features

- hotkeys for responses, problem inspection, etc.
- greeting toggle for responses

### Planned features

- match question with possible answers by keywords in question text, propose options
- notify about new questions

## ChatModerator bot

- search for "ОДОБРИТЬ" buttons, display messages that contain these buttons
- add hotkeys to approve or skip the message in question
- display message in a separate program window, so the chat does not have to be scrolled
- sound notification about new messages if no messages have appeared in the last 2 seconds

## Brief module description

- tui - Custom terminal UI
  - getch - Get a single character from stdin, used in tui
- faq - Manage faq.json and provide response recommendations
- web_plug - Connect to the browser
- quna - Entry point

## TODO:

- add functionality to send bot into waiting mode, refresh page every 5 minutes, ring bell if questions found

- make interface asynchronous
- add better response matching algorithm
- add functionality to pick response from a list
