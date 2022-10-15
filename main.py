from primary_codes import intent_classifier
from primary_codes import entity_classifier
from response import *
import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
import csv
from flask import Flask, request, render_template
from flask_cors import CORS
from collections import defaultdict
import random
import string
import re
import random
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template('index.html')
@app.route("/get")

def init():
    question=request.args['chatinput']
    question=question.lower()
    for r in ((" tata", ""), ("hadis", "dalil"), ("hadits", "dalil"), (" bot", ""), ("gimana", "bagaimana"), (" sih", ""), (" kok", ""), (" oh", "")):
        question = question.replace(*r)
    return tes(question)


def tes(question):

    question = question
    queslow = question.lower()
    ques = re.sub(r'[^\w\s]', '', queslow)
    ques = ques.replace(" bot","")
    if ques in GREETING_INPUTS:
        index = GREETING_INPUTS.index(ques)
        greet = GREETING_RESPONSES[index]
        return greet
    elif (ques == "random fact") :
        out=random.choice(hadis_list)
        return out
    elif (ques == "siapa eksyarbot") :
        return profile
    elif (ques == "apa itu ekonomi syariah") :
        return definisi
    else:
        return answer(question)

def answer(question):
# prediksi intent
    intent = intent_classifier.predict(question)
    if intent != "NULL" :
        return answer_process(question,intent)

# prediksi entitas
def answer_process(question, intent):

    entity = entity_classifier.entity(question,intent)

    read_file = open("data/chatbot_eksyar.json", "r", encoding='UTF8')
    data = json.load(read_file)
    ite = data['items']
    if type(entity) == str:
        # print('entity=' + entity)
        for d in ite:
            if entity.lower() == d['questions'].lower():
                 if intent == "bank":
                    return(d['answers'])
                    intent = "NULL"
                    break
                 elif intent == "investasi":
                    return(d['answers'])
                    intent = "NULL"
                    break
                 elif intent == "reksadana":
                    return(d['answers'])
                    intent = "NULL"
                    break
                 elif intent == "asuransi":
                    return(d['answers'])
                    intent = "NULL"
                    break
                 elif intent == "ekonomi syariah":
                    return(d['answers'])
                    intent = "NULL"
                    break
    else:
        if len(entity)>0:
            ans = []
            for i in entity:
                ans.append(entity[i])
            return str(ans)
    return "Maaf, eksyarbot belum tahu jawaban dari pertanyaanmu. Coba tanyakan pertanyaan lain! Kamu bisa ajukan pertanyaanmu ke rizkaalawiyah88@gmail.com agar bisa terjawab nanti oleh eksyarbot :)"
 


if __name__ == "__main__":
    app.run(debug=True)


