import nltk
import json
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

with open('news.json', encoding="utf8") as fnews:
    data = json.load(fnews)


places = []
def extraction(text):
    stop_words = set(stopwords.words('english'))

    words = word_tokenize(text)


    filtered_sentence = [w for w in words if not w in stop_words]


    pos_tag = nltk.pos_tag(filtered_sentence)

    #print(pos_tag)

    code = []
    for i in pos_tag:
        if i[1] == 'NNP' or i[1] == 'JJ' or i[1] == 'NNPS' or i[1] == 'VBP' or i[1] == 'NN':
            code.append(i[0])
        
    if 'COVID-19' in code:
        code.remove('COVID-19')

    #print(code)

    nes = nltk.ne_chunk(pos_tag)

    name = []
    for ne in nes:
        if type(ne) is nltk.tree.Tree:
            if ne.label() in ['GPE', 'LOCATION']:
                name.append(u' '.join([i[0] for i in ne.leaves()]))

    #print(name)


    for i in code:
        if i not in name:
            name.append(i)
    
    with open("countries.json") as f:
        data = json.load(f)

    for i in name:
        for country in data:
            if re.match(country['name'], i) or re.match(country['code'], i):
                places.append(country['code'])
    


for i in data:
    try:
        if 'countryCode' not in i or  i['countryCode'] == "" :
            extraction(i['header'])
            
    except KeyError as k:
        continue

print(places)