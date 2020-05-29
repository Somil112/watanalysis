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
    temp = ''
    for i in range(len(chat)):
        if (re.match(r'^\d\d\/\d\d\/\d\d',chat[i]) and (temp is None)):
            # Initialize Temp
            temp = chat[i]
        elif (re.match(r'^\d\d\/\d\d\/\d\d',chat[i]) and (temp is not None)):
            
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
#            print("Removed {}".format(chat[i]))
            
    chat = clean_chat
        
#    print("Length of Chat: {}".format(len(chat)))
#    print('\n'.join(chat[:250]))
    
    # for i in range(len(chat)):
    data = {}
    temp = {}
    all_text = []
    for i in range(1,len(chat)):
        ts = datetime.strptime(chat[i].split('-',1)[0].strip(),"%d/%m/%y, %I:%M %p")
        unprocessed_text = chat[i].split('-',1)[1].strip().split(':',1)[1]
        
        # Calculating Word Frequency of Each Chat
        words = len(unprocessed_text.split(' '))
#        text = preprocess(unprocessed_text)
#        all_text += text
        """
        RESTRUCTURE CODE SUCH THAT THE PREPROCESS FUNCTION IS CALLED THE LEAST NO OF TIMES
        """
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
        
        




