# coding: utf-8

from __future__ import print_function

import os
import sys
import numpy as np
from bottle import route, post, run, template, request, response
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pickle

MAX_SEQUENCE_LENGTH = 1000

model = load_model('my_model_trained_x8.h5')

with open('tokenizerx8.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

labels_index={'alt.atheism': 0, 'comp.graphics': 1, 'comp.os.ms-windows.misc': 2, 'comp.sys.ibm.pc.hardware': 3, 'comp.sys.mac.hardware': 4, 'comp.windows.x': 5, 'misc.forsale': 6, 'rec.autos': 7, 'rec.motorcycles': 8, 'rec.sport.baseball': 9, 'rec.sport.hockey': 10, 'sci.crypt': 11, 'sci.electronics': 12, 'sci.med': 13, 'sci.space': 14, 'soc.religion.christian': 15, 'talk.politics.guns': 16, 'talk.politics.mideast': 17, 'talk.politics.misc': 18, 'talk.religion.misc': 19}

inv_labels_index={}
for category, index in labels_index.items():
    inv_labels_index[index] = category

def predict(text):
    predict_texts = []  # list of text samples"

    predict_texts.append(text)
    print(predict_texts)

    predict_sequences = tokenizer.texts_to_sequences(predict_texts)
    predict_data = pad_sequences(predict_sequences, maxlen=MAX_SEQUENCE_LENGTH)
    print('Shape of predict data tensor:', predict_data.shape)

    x_predict = predict_data
    print(x_predict)

    y_predict = model.predict(x_predict)

    results = {}

    for x in y_predict:
        for index, y in enumerate(x):
            category = inv_labels_index[index]
            results[category] = float(y)
            print('{0} -> {1:.20f}'.format(category, y))

    max_val = np.argmax(y_predict)


    for name, age in labels_index.items():
        if age == max_val:

            print('Category it belongs to : ',name)


    print('Cat_ID : ' ,max_val)

    print(results)
    return results

@route('/api/classify-article', method=['OPTIONS', 'POST'])
def classify_article():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

    if request.method == 'OPTIONS':
        return {}

    article = request.json
    print(article)
    text = article['text']

    resultDict = predict(text)

    return {
        "predictions": resultDict
    }


run(host='localhost', port='8080', server='wsgiserver')
