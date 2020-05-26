import numpy as np
import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt
import re
import gensim
from datetime import datetime
import json
np.random.seed(400)


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




def create_empty_hours():
    data = {}
    for i in range(24):
        data[str(i).zfill(2)] = {"total_words":0}
        
    return data

def process(file):
    chat = file.read().decode('utf-8')
    #chat = file.read().decode('utf-8')
    chat = chat.splitlines()
    print('Length of Chat: {}\n'.format(len(chat)))
    print('\n'.join(chat[:10]))
   
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
    
    # for i in range(len(chat)):
    data = {}
    
    for i in range(1,len(chat)):
        ts = datetime.strptime(chat[i].split('-',1)[0].strip(),"%d/%m/%y, %I:%M %p")
        words = len(chat[i].split('-',1)[1].strip().split(' '))
        year = str(datetime.strftime(ts,"%Y"))
        month = datetime.strftime(ts,"%B")
        day = str(datetime.strftime(ts,"%d"))
        hour = str(datetime.strftime(ts,"%H"))
    
        if year not in data.keys():
            data[year] = {"total_words": words,"months":{}}
        else:
            data[year]["total_words"] += words
        
        if month not in data[year]["months"].keys():
            data[year]["months"][month] = {"total_words":words,"days":{}}
        else:
            data[year]["months"][month]["total_words"] += words
            
        if day not in data[year]["months"][month]["days"].keys():
            data[year]["months"][month]["days"][day] = {"total_words":words,"hours":create_empty_hours()}
        else:
            data[year]["months"][month]["days"][day]["total_words"] += words
        
        if hour not in data[year]["months"][month]["days"][day]["hours"].keys():
            data[year]["months"][month]["days"][day]["hours"][hour] = {"total_words":words}
        else:
            data[year]["months"][month]["days"][day]["hours"][hour]["total_words"] += words
      
    return data
