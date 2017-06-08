"""."""
# from nltk.corpus import sentiwordnet as swn


# print(list(swn.senti_synset('slow.v.02')))
import requests

data = [
    ('text', 'suck it')
]

print(requests.post('http://text-processing.com/api/sentiment/', data=data).text)
