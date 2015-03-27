from iknow.trie import Trie

__author__ = 'gary'

import unittest


class MyTestCase(unittest.TestCase):
    def test_add_and_search(self):
        trie = Trie()

        trie.add("tree", "data1")
        trie.add("trie", "data2")
        trie.add("treap", "data3")

        self.assertEqual(trie.search("tree"), "data1")
        self.assertEqual(trie.search("trie"), "data2")
        self.assertEqual(trie.search("treap"), "data3")

    def test_immutable(self):
        trie = Trie()
        trie.add("trie", "data1")
        trie.add("trie", "data2")

        self.assertEqual(trie.search("trie"), "data1")

    def test_references_modify(self):
        trie = Trie()

        trie.add("list", [])
        f = trie.search("list")
        f.append(3)

        self.assertEqual(trie.search("list"), [3])


if __name__ == '__main__':
    unittest.main()
