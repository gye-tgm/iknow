from loremipsum import Generator


FILE = 'sentences.txt'
NUM_SENTENCES = 1000000

with open('dictionary.txt', 'r') as dict_file:
    dict = dict_file.read().split()

g = Generator(dictionary=dict)

with open(FILE, 'w') as out_file:
    for i in range(NUM_SENTENCES):
        print(i)
        out_file.write(g.generate_sentence()[2] + '\n')
