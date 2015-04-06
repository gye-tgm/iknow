from iknow.resources.entrymanager import EntryManager, Entry

__author__ = 'gary'

f = open("sentences.txt", "r")
em = EntryManager()

for line in f:
    em.add_entry(Entry(line))

"""
FILE = 'sentences.txt'
NUM_SENTENCES = 10

with open('dictionary.txt', 'r') as dict_file:
    dict = dict_file.read().split()

g = Generator(dictionary=dict)
em = EntryManager()

with open(FILE, 'w') as out_file:
    for i in range(NUM_SENTENCES):
        sentence = g.generate_sentence(start_with_lorem=True)[2] + '\n'
        em.add_entry(Entry(sentence))
        print(sentence)

print("Found the following")

for x in em.search_entries('lorem'):
    print(x.text)

"""