import json


class FAQManager:
    """
    FAQManager is responsible for storage and updates of the local faq.json file.

    Allowed methods:
        - update_faq(new_reply, question_header)
        - get_responses(question: str) -> list
    """

    def __init__(self, faq_file: str) -> None:
        self.faq_file = faq_file
        with open(self.faq_file, "r") as file:
            self.faq = json.load(file)

    def update_faq(self, new_reply: str, question: str):
        """ Updates the existing faq with new_faq data. """
        if new_reply[0] == 'g':
            self.faq['general'].append(new_reply[1:])
        elif question not in self.faq:
            self.faq[question] = [new_reply]
        else:
            self.faq[question].append(new_reply)
        with open(self.faq_file, "w") as file:
            json.dump(self.faq, file, ensure_ascii=False)

    def get_responses(self, question: str):
        """Returns a list of possible replies."""
        matches = self.faq.get(question, []) + self.faq["general"]
        return matches

