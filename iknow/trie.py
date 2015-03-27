__author__ = 'gary'

"""
add(word, idx)
remove(word, idx)
"""


class TrieNode(object):
    def __init__(self, char, data=None):
        self.char = char
        self.data = data
        self.children = []

    def find_child(self, char):
        for c in self.children:
            if c.char == char:
                return c
        return None

    def add_child(self, node):
        self.children.append(node)
        return node

        # TODO: deconstructor


class Trie(object):
    def __init__(self):
        self.root = TrieNode('$')

    def add(self, word, data):
        cur = self.root
        for c in word:
            cur = cur.find_child(c)
            if cur is None:
                cur = cur.add_child(TrieNode(c))
        cur.data = data

    def search(self, word):
        cur = self.root
        for c in word:
            cur = cur.find_child(c)
            if cur is None:
                return None
        return cur.data

