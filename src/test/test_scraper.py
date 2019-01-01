import sys
sys.path.append('../')

import unittest
import scraper

class TestScraperFunctions(unittest.TestCase):

    def test_get_string(self):
        self.assertEqual(scraper.get_string('Foo', 'FooBar'), 'Foo')
        self.assertEqual(scraper.get_string('\w+', 'FooBar'), 'FooBar')
        self.assertEqual(scraper.get_string('\d+', 'FooBar'), '')

    def test_get_integer(self):
        self.assertEqual(scraper.get_integer('\d+', 'ABC45FGH'), 45)
        self.assertEqual(scraper.get_integer('\d+', 'ABCDEFGH'), 0)

    def test_get_signed_integer(self):
        self.assertEqual(scraper.get_signed_integer('.\d+', 'Init +4'), 4)
        self.assertEqual(scraper.get_signed_integer('.\d+', 'Init -4'), -4)
        self.assertEqual(scraper.get_signed_integer('.\d+', 'ABCDEF'), 0)

    def test_split_csv(self):
        self.assertEqual(scraper.split_csv('oranges, apples(12, red), bananas'), ['oranges', 'apples(12, red)', 'bananas'])
        self.assertEqual(scraper.split_csv('apples(12, red)'), ['apples(12, red)'])

    def test_get_csv(self):
        self.assertEqual(scraper.get_csv('(?<=Feats ).+', 'Feats One, Two, Three(Four, Five)'), ['One', 'Two', 'Three(Four, Five)'])
        self.assertEqual(scraper.get_csv('(?<=Feats ).+', 'Skills One, Two, Three(Four, Five)'), [])


if __name__ == '__main__':
    unittest.main()
