#!/usr/bin/env python
# coding: utf-8

# In[48]:


import numpy as np
import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt
import re
from nlp_preprocess import *
import gensim
from datetime import datetime
import json
np.random.seed(400)


# In[2]:


# Helper Functions
def chat_printer(arr):
    """
    Used to Print Chat in a Readable Format
    """
    
    printer_arr = []
    for i in range(len(arr)):
        lenchat = len(arr[i][1])
        no_of_chats = min(5,int(lenchat/10))
        line = arr[i][0] + ':\n' + '\n'.join(arr[i][1][:no_of_chats]) + '.......'
        printer_arr.append(line)
        
    return printer_arr

def contact_processor(csv_names):
    """
    Go to contacts.google.com and export as Google CSV
    Import it here
    Used for preprocessing docs
    """
    
    if isinstance(csv_names,list):
        final = []
        for csv_name in csv_names: 
            df = pd.read_csv(csv_name)['Name']
            contact_names = list(set(df.values))
            new = []
            for name in contact_names:
                if str(name) != 'nan':
                    new.append(name)
            final += new
            
        final = set(list(final))
        return final
    elif isinstance(csv_names,str):
        df = pd.read_csv(csv_name)['Name']
        contact_names = list(set(df.values))
        new = []
        for name in contact_names:
            if str(name) != 'nan':
                new.append(name)
                
    return new
    
def get_top_chats(doc,num):
    """
    Get Top X Chats 
    """
    arr =[]
    for i in range(num):
        text = ' '.join(doc[i][1])
        arr.append(text)
        
    return arr


def preprocess(text):
    """
    Text Preprocessing. Uses external function text_preprocess taken from nlp_preprocess.py
    """
    result=[]
    contacts = contact_processor(['contacts_1.csv','contacts_2.csv'])
    prohibitedWords = contacts + ['<Media omitted>']
    big_regex = re.compile('|'.join(map(re.escape, prohibitedWords)))
    the_message = big_regex.sub("", text)
    text = the_message
    result = text_preprocess(text)
    return result


# In[3]:


filename = "conspiracy.txt"
outfile = open(filename,'rb')
chat = outfile.read().decode('utf-8')
chat = chat.splitlines()
print('Length of Chat: {}\n'.format(len(chat)))
print('\n'.join(chat[:10]))
outfile.close()


# In[52]:


json_data = {"most_chatted_day": None, "individual_data":None}


# In[4]:


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

print("Length of Chat: {}".format(len(chat)))
print('\n'.join(chat[:250]))


# In[51]:


from collections import OrderedDict 
# for i in range(len(chat)):
data = OrderedDict()
for i in range(1,len(chat)):
    ts = datetime.strptime(chat[i].split('-',1)[0].strip(),"%d/%m/%y, %I:%M %p")
    words = len(chat[i].split('-',1)[1].strip().split(' '))
    date = datetime.strftime(ts,"%d/%m/%y")
    hour = int(datetime.strftime(ts,"%H"))
    if date not in data.keys():
        data[date] = [0 for i in range(24)]

    data[date][hour] += words

    
maxwords = -999
maxdate = None
for date,lwords in data.items():
    if sum(lwords) > maxwords:
        maxdate = date
        maxwords = sum(lwords)


    


# In[54]:


json_data["most_chatted_day"] = maxdate
json_data["individual_data"] = list(data.items())

json.dumps(json_data)


# In[40]:


data

