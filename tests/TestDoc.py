import unittest
from Doc import *


class TestDoc(unittest.TestCase):
    def setUp(self):
        self.doc = Doc(0)

    def test_parse_sentences(self):
        self.doc.body = ''
        self.assertEquals(self.doc.parse_sentences(), [])
        self.doc.body = 'I love you'
        self.assertTrue(len(self.doc.parse_sentences()), 1)

    def test_parse_words(self):
        self.doc.body = ''
        self.assertEquals(self.doc.parse_words(), [])
        self.doc.body = 'I love you'
        self.assertEquals(self.doc.parse_words(), ['i', 'love', 'you'])

    @unittest.skip('test')
    def test_text_file(self):
        with open('sampleText.txt', 'r') as inputfile:
            self.doc.body = inputfile.read()

if __name__ == '__main__':
    unittest.main()
