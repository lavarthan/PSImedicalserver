print("Please be patient while system loading.....")

# to avoid the unwanted warnings
# import logging
# import os
# logging.disable(logging.WARNING)
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# import warnings
# warnings.simplefilter(action='ignore', category=FutureWarning)
# import sys
# stderr = sys.stderr
# sys.stderr = open(os.devnull, 'w')
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# import the libraries needed for the chatbot
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
import pandas as pd
import random
from sklearn.externals import joblib
import json

# import the function from other files
from extractor import extractor
from speech_recognizer import text_to_speech
from speech_recognizer import speech_to_text
from database_details import insert_details
from database_details import get_database_details

stemmer = LancasterStemmer()
words = []
classes = []
documents = []
ignore_words = ['?']

with open('Dataset.json') as json_file:
    intents = json.load(json_file)

for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

training = []
output_empty = [0] * len(classes)
for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]

    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])
random.shuffle(training)
training = np.array(training)
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# define our model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
try:
    # instead training the model every time we can save the model and can be used
    # model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=0)
    # joblib.dump(model, 'my_model.pkl')
    # joblib.dump((words, ignore_words, classes, documents), 'my_data.pkl')
    model = joblib.load('my_model.pkl')
    words, ignore_words, classes, documents = joblib.load('my_data.pkl')

except:
    # in case we don't have the trained model we first train and save the model
    model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=0)
    joblib.dump(model, 'my_model.pkl')
    joblib.dump((words, ignore_words, classes, documents), 'my_data.pkl')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                # if show_details:
                #     print("found in bag: %s" % w)
    return np.array(bag)


def get_results(sentence):
    ERROR_THRESHOLD = 0.9
    try:
        input_data = pd.DataFrame([bow(sentence, words)], dtype=float, index=['input'])
        results = model.predict([input_data])[0]
        results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
        # print(results)
        results.sort(key=lambda x: x[1], reverse=True)

        return_list = []
        for r in results:
            return_list.append((classes[r[0]], str(r[1])))

        if len(return_list[0]) == 0:
            return [('noanswer', 0.870264)]
        return return_list
    except IndexError:
        return [('noanswer', 0.870264)]


def get_response(x, inp):
    for i in range(len(intents['intents'])):
        if intents['intents'][i]["tag"] == x and i < 10:
            print(random.choice(intents['intents'][i]["responses"]))
        elif intents['intents'][i]["tag"] == x and i == 10:
            print(random.choice(intents['intents'][i]["responses"]))
            complain = input()
            insert_details(complain)

        elif intents['intents'][i]["tag"] == x and i > 10:
            details = extractor(inp)
            # print(details)
            print(get_database_details(x, details))


def response(messageText):
    try:
        question = get_results(messageText)[0][0]
        return get_response(question, messageText)
    except:
        return "Error has occured with the Banking server. Sorry about that!"

# print("Welcome to the Government Medical Inquiry Service")
# choose = input("Choose the way you want to interact(type 1 or 2):\n1. Text\n2. Audio\n")
# if choose == "1":
#     x = input("How can I help you?\n (type 'quit' to exit!)\n")
#     while x != 'quit':
#         # identify the correct tag
#         question = get_results(x)[0][0]
#         get_response(question, x)
#         x = input("")
# elif choose == "2":
#     print("How can I help you?\n(say 'quit' to exit!)")
#     text_to_speech("How can I help you?   (say 'quit' to exit!)")
#     x = ""
#     while x != 'quit':
#
#         x = speech_to_text()
#         if x == "quit":
#             pass
#         elif x == "I couldn't hear anything":
#             print("sorry I didn't catch that..\nsay again\n")
#             text_to_speech("sorry I didn't catch that.. say again\n")
#
#         else:
#             question = get_results(x)[0][0]
#             print(get_response(question, x),"\n")
#             text_to_speech(get_response(question, x))
#             text_to_speech("Press Enter key to continue")
#             input("\nPress any key to continue...")
#
# print("Thank you for using our service!")
# text_to_speech("Thank you for using our service!")
