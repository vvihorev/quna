import re

import spacy


nlp = spacy.load("ru_core_news_sm")


def get_question_tokens(question: str) -> list:
    question = re.sub(r'[^ \w]|\d', '', question)
    return [token.lemma_ for token in nlp(question) if not token.is_stop]


tokens = get_question_tokens("Пожалуйста, помогить установить python 3.8.10 себе на комп.")
faq = {"Пожалуйста, напишите администраторам.": ["загружать", "отправить", "открыть", "установить"]}
for value in faq.values():
    print(len(set(value) & set(tokens)))
