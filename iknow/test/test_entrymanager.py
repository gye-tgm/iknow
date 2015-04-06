from iknow.resources.entrymanager import EntryManager, Entry

__author__ = 'gary'

import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        em = EntryManager()
        em.add_entry(Entry("A song of ice and fire"))
        em.add_entry(Entry("A song by me"))
        print(em.search_entries("SONG"))


if __name__ == '__main__':
    unittest.main()
