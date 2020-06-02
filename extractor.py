import nltk
import spacy
import en_core_web_sm

from date_extractor import date_extractor


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent


nlp1 = en_core_web_sm.load()
nlp2 = spacy.load("custom")

def extractor(input):
    doc1 = nlp1(input)
    doc2 = nlp2(input)
    arr1 = [(X.text, X.label_) for X in doc1.ents]
    arr2= [(X.text, X.label_) for X in doc2.ents]
    # print(arr1)
    # print(arr2)
    arr = list(set(arr1+arr2))

    result = []
    for i in arr:
        if i[1] == 'PERSON' and i[0] not in ["Mannar", "Kandy"]:
            # print("Name is", i[0])
            result.append(i)
        elif i[1] == 'DATE':
            date = date_extractor((i[0]).split()[-1])
            # print("Date is", date)
            result.append((date, 'DATE'))
        elif i[1] == 'TIME':
            # print("Time is", i[0])
            result.append(i)
    for i in arr2:
        if i[1] == 'GPE':
            # print("Location is",i[0])
            result.append(i)

    return result