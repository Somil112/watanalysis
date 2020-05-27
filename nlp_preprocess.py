from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from num2words import num2words
from nltk.stem import WordNetLemmatizer 
import demoji
demoji.download_codes()
import numpy as np
from hinglish_stopwords import get_hinglish_stopwords



import spacy
nlp = spacy.load("en_core_web_sm")

# Lower Casing the Data
def convert_lower_case(data):
    return np.char.lower(data)

# Removing Stop Words
def remove_stop_words(data):
    stop_words = stopwords.words('english') + get_hinglish_stopwords()
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text

# Remove Punctuations
def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

# Remove Apostrophe
def remove_apostrophe(data):
    return np.char.replace(data, "'", "")

# Stemming
def stemming(data):
    stemmer= PorterStemmer()
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text


def lemmatize(data):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + lemmatizer.lemmatize(w)
        
    return new_text

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text


def spacy_preprocess(text):
    text = nlp(text)
    candidate_pos = ['NOUN', 'PROPN', 'VERB']
    jd = []
    for token in text:
        if token.pos_ in candidate_pos and token.is_stop is False:
            jd.append(str(token))

    return jd

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist


def preprocess(data): 
    data = convert_lower_case(data)
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = remove_punctuation(data)
    data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
    data = lemmatize(data)
    data = demoji.replace(str(data).strip(),'')
    data = spacy_preprocess(data)
    return data