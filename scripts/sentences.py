from iknow.app import *
from loremipsum import Generator
import random
import sys

FILE = 'sentences.txt'
NUM_SENTENCES = 10**6

dictfile = sys.argv[1]

with open(dictfile, 'r') as dict_file:
    dict = dict_file.read().split()

g = Generator(dictionary=dict)

for i in range(NUM_SENTENCES):
    print(i)

    sentence = g.generate_sentence()[2]
    k = Knowledge(sentence) 
    k.tags = []
    tagstr = [random.choice(dict) for x in range(5)]
    for t in tagstr:
        x = Tag.query.filter_by(id=t).first()
        if x is None:
            x = Tag(t)
            db.session.add(x)
        k.tags.append(x)
    db.session.add(k)
    db.session.commit()

