import unittest
from entities.Doc import *


class TestDoc(unittest.TestCase):
    def setUp(self):
        self.doc = Doc(doc_id=0)

    def test_parse_sentences(self):
        self.doc.body = ''
        self.assertEqual(self.doc.parse_sentences(), [])
        self.doc.body = 'I love you'
        self.assertTrue(len(self.doc.parse_sentences()), 1)

    def test_parse_words(self):
        self.doc.body = ''
        self.assertEqual(self.doc.parse_words(), [])
        self.doc.body = 'I love you'
        self.assertEqual(self.doc.parse_words(), ['i', 'love', 'you'])

if __name__ == '__main__':
    unittest.main()
