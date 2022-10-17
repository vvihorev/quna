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

    def update_faq(self, new_faq: dict):
        """
        Updates the existing faq with new_faq data.
        new_faq format: [question string: keywords list]
        """
        self.faq.update(new_faq)
        with open(self.faq_file, "w") as file:
            json.dump(self.faq, file)

    def _word_match(self, w1: str, w2: str):
        """Returns probability of two words being the same."""
        return round(
            len([p for p in zip(w1, w2) if p[0] == p[1]]) / min(len(w1), len(w2)), 2
        )

    def _token_match(self, question_tokens: set, reply_tokens: set):
        """
        Returns a probability of two sets of tokens matching.
        Depends on the size of the second set.
        """
        return round(len(question_tokens & reply_tokens) / len(reply_tokens), 2)

    def _get_question_tokens(self, question: str) -> set:
        """Gets a set of tokens from an input string"""
        question = question.lower()
        question = re.sub(r"[^ \w]|\d  ", " ", question)
        tokens = [word for word in question.split() if len(word) > 4]
        return set([re.sub(r"[аеиоуюяэьый]", "", token) for token in tokens])

    def get_responses(self, question):
        """Returns a list of possible responses in order of decreasing likeliness of match."""
        question_tokens = self._get_question_tokens(question)
        matches = []
        for pair in self.faq.items():
            # TODO: reply tokens can be cached, not calculated each time
            reply_tokens = self._get_question_tokens(" ".join(pair[1]))
            match = self._token_match(question_tokens, reply_tokens)
            matches.append((match, pair[0]))
        matches.sort(key=(lambda x: x[0]))
        return matches[::-1]
