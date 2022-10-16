import spacy


nlp = spacy.load("ru_core_news_sm")

with open("sample_questions", "r", encoding="utf-8") as file:
    lines = file.readlines()
for line in lines:
    # print(token.text, token.pos_, token.dep_)
    res = [token.lemma_ for token in nlp(line) if not token.is_stop]
    print(res)

