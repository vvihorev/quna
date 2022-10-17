import json
import re


def word_match(w1: str, w2: str):
    return len([p for p in zip(w1, w2) if p[0] == p[1]]) / min(len(w1), len(w2))


def token_match(question_tokens: set, reply_tokens: set):
    return len(question_tokens & reply_tokens)/len(reply_tokens)


def get_question_tokens(question: str) -> set:
    question = question.lower()
    question = re.sub(r'[^ \w]|\d  ', ' ', question)
    tokens = [word for word in question.split() if len(word) > 4]
    return set([re.sub(r'[аеиоуюяэьый]', '', token) for token in tokens])


def get_responses(question, faq):
    question_tokens = get_question_tokens(question)
    matches = []
    for pair in faq.items():
        reply_tokens = get_question_tokens(' '.join(pair[1]))
        match = token_match(question_tokens, reply_tokens)
        matches.append((match, pair[0]))
    matches.sort(key=(lambda x: x[0]))
    return matches[::-1]


question = "Пожалуйста, помогить установить python 3.8.10 себе на комп."
with open('faq.json', 'r') as file:
    faq = json.load(file)
print(get_responses(question, faq))
# with open('faq.json', 'w') as file:
    # json.dump(faq, file)
