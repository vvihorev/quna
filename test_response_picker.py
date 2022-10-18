import json
import re


def get_question_tokens(question: str) -> set:
    """Gets a set of tokens from an input string"""
    question = question.lower()
    question = re.sub(r"[^ \w]|\d  ", " ", question)
    tokens = [word for word in question.split() if len(word) > 4]
    return set([re.sub(r"[аеиоуюяэьый]", "", token) for token in tokens])


def token_match(question_tokens: set, reply_tokens: set):
    return round(len(question_tokens & reply_tokens) / len(reply_tokens), 2)


with open('faq.json', "r") as file:
    faq = json.load(file)


question = "Пожалуйста помогите, не могу решить задачу квадрат, кольцо"
question_tokens = get_question_tokens(question)
matches = []
for pair in faq.items():
    reply_tokens = get_question_tokens(" ".join(pair[1]))
    match = token_match(question_tokens, reply_tokens)
    matches.append((match, pair[0]))
matches.sort(key=(lambda x: x[0]))

for i, m in enumerate(matches[::-1]):
    print(f"{i}: {m[0]}, {m[1]}")
x = int(input("which?"))
print(matches[x]) 

