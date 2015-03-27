from loremipsum import Generator


FILE = 'sentences.txt'
NUM_SENTENCES = 1000

with open('dicitionary.txt', 'r') as dict_file:
    dict = dict_file.read().split()

g = Generator(dictionary=dict)

with open(FILE, 'w') as out_file:
    for i in range(NUM_SENTENCES):
        out_file.write(g.generate_sentence()[2] + '\n')
