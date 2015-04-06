__author__ = 'gary'

from iknow.resources.trie import Trie


class Entry(object):
    def __init__(self, text):
        self.text = text


class EntryManager(object):
    def __init__(self):
        self.trie = Trie()
        self.entries = []

    def add_entry(self, entry):
        idx = len(self.entries)
        for word in entry.text.lower().split(" "):
            self.trie.add(word, set())
            self.trie.search(word).add(idx)
        self.entries.append(entry)

    def search_entries(self, word):
        idx = self.trie.search(word.lower())
        if idx is None:
            return []
        return [self.entries[i] for i in idx]