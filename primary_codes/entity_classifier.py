# from rake_nltk import Rake
import nltk
from multi_rake import Rake
from spacy.lang.id import Indonesian
import spacy
import pytest
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from string import punctuation
import string
from nltk.tokenize import word_tokenize
import re

def data():
    with open("data/entities/bank.txt", "r", encoding='UTF8') as title1:
        title = title1.readlines()
    return title

def data2():
    with open("data/entities/investasi.txt", "r", encoding='UTF8') as title1:
        title = title1.readlines()
    return title

def data3():
    with open("data/entities/reksadana.txt", "r", encoding='UTF8') as title1:
        title = title1.readlines()
    return title

def data4():
    with open("data/entities/asuransi.txt", "r", encoding='UTF8') as title1:
        title = title1.readlines()
    return title

def data5():
    with open("data/entities/ekonomi_syariah.txt", "r", encoding='UTF8') as title1:
        title = title1.readlines()
    return title

def phrase(ques):
    phrase1 = []
    new_list = []
    factory = StopWordRemoverFactory()
    stop_word_list = factory.get_stop_words()
    stopwordnya = list(punctuation)+stop_word_list
    with pytest.raises(NotImplementedError):
        Rake(language_code='xxx')

    rake_id = Rake(
        min_chars=3,
        max_words=4,
        min_freq=1,
        language_code='id',
        stopwords=stopwordnya
    )

    question=ques.lower()
    result = rake_id.apply(question)
    phrase1 = min(result)

    for items in phrase1:
        new_list.extend(str(items).lower().split())
    return phrase1, new_list


def lis(l,intent):
    new_l = l
    ans = []
    """yang ini ganti datanya pake parameter dari server sesuai intent"""
    if intent=="bank":
        title=data()
    elif intent=="investasi":
        title=data2()
    elif intent=="reksadana":
        title=data3()
    elif intent=="asuransi":
        title=data4()
    elif intent=="ekonomi syariah":
        title=data5()

    for i in new_l:
        i = str(i).lower().strip("\n")
        for t in title:
            t = t.lower()

            if i in t:
                ans.append(t.strip("\n"))

    ans = list(set(ans))
    return ans


def finalA(ques, ans):
    count = 0
    for i in ans:

        i = i.strip("\n").lower()
        if i in ques.lower():
            if ques.lower() in i:
                count = count + 1
                ent = i
                break
            else:
                count = count + 1
                ent = i
                break
    if count == 1:
        return ent
    else:
        if len(ans) == 1:
            abc = ans[0]
            abc = abc.lower().strip("\n")
            return abc
        else:
            ansD = {}
            # print("pilih yang ada di bawah ini")
            for i in range(len(ans)):
                ansD[i + 1] = ans[i]
            return ansD


def entity(ques,intent):

    ph, list_p = phrase(ques)
    ans1 = lis(ph,intent)
    ans = lis(list_p,intent)
    y = finalA(ques, ans1)
    if len(ans1) == 0 and len(y) == 0:
        y = finalA(ques, ans)
        return y
    elif len(ans) == len(ans1):
        y = finalA(ques, ans)
        return y
    else:
        y = finalA(ques, ans1)
        return y

# question = input("Masukan pertanyaan :")
# intent = input("Masukan intent :")
# print(entity(question,intent))
# print(phrase(question.lower()))
