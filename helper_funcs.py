import numpy as np

import re

import gensim
from datetime import datetime

from nlp_preprocess import *

np.random.seed(400)

## Remove Links in preprocessing


def create_empty_hours():
    data = {}
    for i in range(24):
        data[str(i).zfill(2)] = {"total_words":0}
        
    return data

def process(file):
    chat = file.read().decode('utf-8')
    #chat = file.read().decode('utf-8')
    chat = chat.splitlines()
    
    new_chat = []
    temp = None
    for i in range(len(chat)):
        
        if (re.match(r'^\d{1,2}\/\d{1,2}\/\d{2}',chat[i]) and temp is None):
            
            
            temp = chat[i]
        elif (re.match(r'^\d{1,2}\/\d{1,2}\/\d{2}',chat[i]) and temp is not None):
            
            # Append Temp to Chat and Initialize new Temp with current Chat
            new_chat.append(temp)
            temp = chat[i]
        else:
            temp += chat[i]
            
    
    chat = new_chat
    
    clean_chat = []
    for i in range(1,len(chat)):
        try:
            temp = chat[i].split('-',1)[1].strip().split(':',1)[1]
            clean_chat.append(chat[i])
        except:
            pass

            
    chat = clean_chat
    
    dateformat = ["%d/%m/%y", "%m/%d/%y","%d/%m/%Y","%m/%d/%Y"]
    timeformat = ["%I:%M %p","%H:%M"]
   
    dchoice = None
    tchoice = None
    year = len(chat[0].split('-',1)[0].strip().split(',')[0].strip().split('/',2)[2].strip())
    
    for i in range(min(len(chat),200)):
        ts = chat[i].split('-',1)[0].strip().split(',')
        datecheck = int(ts[0].strip().split('/',2)[1])
        timecheck = int(ts[1].strip().split(':',1)[0])
        if datecheck > 12:
            if year == 4:
                dchoice = 3
            else:
                dchoice = 1
            break
        
    if dchoice is None:
        if year > 2:    
            dchoice = 2
        else:
            dchoice = 0
            
            
        
    for i in range(200):
         ts = chat[i].split('-',1)[0].strip().split(',')
         timecheck = int(ts[1].strip().split(':',1)[0])
         if timecheck > 12:
             tchoice = 1
             break
        
    if tchoice is None:
        tchoice = 0
            
         
    dtformat = dateformat[dchoice] + ", " + timeformat[tchoice]

    data = {}
    temp = {}
    all_text = []
    for i in range(1,len(chat)):
        ts = datetime.strptime(chat[i].split('-',1)[0].strip(),dtformat)
        unprocessed_text = chat[i].split('-',1)[1].strip().split(':',1)[1]
        
        words = len(unprocessed_text.split(' '))

        year = str(datetime.strftime(ts,"%Y"))
        month = datetime.strftime(ts,"%B")
        day = str(datetime.strftime(ts,"%d"))
        hour = str(datetime.strftime(ts,"%H"))
    
        
        if year not in data.keys():
            data[year] = {"total_words": words,"months":{},"all_words": []}
            temp[year] = {"text":unprocessed_text,"months":{}}
        else:
            data[year]["total_words"] += words
            temp[year]["text"] += unprocessed_text
        
        if month not in data[year]["months"].keys():
            data[year]["months"][month] = {"total_words":words,"days":{},"all_words":[]}
            temp[year]["months"][month] = {"text":unprocessed_text}
        else:
            data[year]["months"][month]["total_words"] += words
            temp[year]["months"][month]["text"] += unprocessed_text
            
        if day not in data[year]["months"][month]["days"].keys():
            data[year]["months"][month]["days"][day] = {"total_words":words,"hours":create_empty_hours()}
        else:
            data[year]["months"][month]["days"][day]["total_words"] += words
        
        if hour not in data[year]["months"][month]["days"][day]["hours"].keys():
            data[year]["months"][month]["days"][day]["hours"][hour] = {"total_words":words}
        else:
            data[year]["months"][month]["days"][day]["hours"][hour]["total_words"] += words
            
    bestyear = max(data,key=lambda x:data[x]["total_words"])
    
    maxvalyear = data[bestyear]["total_words"]
    
    all_text = []
    bestmonths = []
    for year in list(data.keys()):
        ywords = []
        for month in data[year]["months"].keys():
            mwords = preprocess(temp[year]["months"][month]["text"]) 
            data[year]["months"][month]["all_words"] = mwords
            ywords += mwords
        data[year]["all_words"] = ywords
        all_text += ywords
    
        temp2 = data[year]["months"]
        month = max(temp2,key=lambda x: temp2[x]["total_words"])
        maxvalmonth = temp2[month]["total_words"]
        bestmonths.append({"year":year,"month":month,"value":maxvalmonth})
        data[year]["maxval"] = maxvalmonth
    return {"data":data,"corpus":all_text,"maxval":maxvalyear,"best_year":{"year":bestyear,"value":maxvalyear},"best_months":bestmonths}


def topics(words,corpus):
    dictionary = gensim.corpora.Dictionary([corpus])
    bow_corpus = [dictionary.doc2bow(words)]
    lda_model =  gensim.models.LdaMulticore(bow_corpus, 
                                   num_topics = 10, 
                                   id2word = dictionary,                                    
                                   passes = 2,
                                   workers = 2)
    topic = lda_model.show_topic(0,200)
    wctopic = []
    for i in range(len(topic)):
        wctopic.append({"text":topic[i][0],"value":str(topic[i][1])})
        
    return wctopic
        
