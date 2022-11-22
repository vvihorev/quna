from typing import List
import json
import re


class FAQManager:
    """
    FAQManager is responsible for storage and updates of the local faq.json file.

    Allowed methods:
        - update_faq(new_faq)
        - get_responses(question: str) -> list

    Example usage:
        question = "Пожалуйста, помогить установить python 3.8.10 себе на комп."
        faq = FAQManager('faq.json')
        faq.get_responses(question)
    """

    def __init__(self, faq_file: str) -> None:
        self.faq_file = faq_file
        with open(self.faq_file, "r") as file:
            self.faq = json.load(file)

    def update_faq(self, new_reply: str, question: str):
        """
        Updates the existing faq with new_faq data.
        """
        q_topic = self._get_question_topic(question)
        if q_topic not in self.faq:
            self.faq[q_topic] = [new_reply]
        else:
            self.faq[q_topic].append(new_reply)
        with open(self.faq_file, "w") as file:
            json.dump(self.faq, file, ensure_ascii=False)

    def get_responses(self, question: str):
        """Returns a list of possible responses in order of decreasing likeliness of match."""
        matches = self.faq.get(question, [])
        for m in self.faq["general"]:
            if m[:7] == 'general':
                m = m[:7]
            matches.append(m)
        return matches

