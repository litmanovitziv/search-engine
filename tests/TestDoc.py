import unittest
from search.Doc import *


class TestDoc(unittest.TestCase):
    def setUp(self):
        self.doc = Doc(doc_id=0)

    def test_set_histogram(self):
        self.doc.set_histogram(list(map(str.strip, 'love you like you'.split())))
        self.assertEqual([*self.doc.histogram], ['love', 'you', 'like'])
        self.assertDictEqual(self.doc.histogram, dict(love=dict(tf=1), you=dict(tf=2), like=dict(tf=1)))

    def test_set_token_weight(self):
        self.doc.set_histogram(list(map(str.strip, 'love you like you'.split())))
        self.doc.set_token_weight('you', 0.5)
        self.assertEqual(self.doc.get_term_metrics('you').get('w'), 1)

    def test_parse_sentences(self):
        self.doc._body = ''
        self.assertEqual(self.doc.parse_sentences(), [])
        self.doc._body = 'I love you'
        self.assertTrue(len(self.doc.parse_sentences()), 1)

    def test_parse_words(self):
        self.doc.body = ''
        self.assertEqual([*self.doc.histogram], [])
        self.doc.body = 'I love you. I like you'
        self.assertEqual([*self.doc.histogram], ['love', 'you', 'like'])


if __name__ == '__main__':
    unittest.main()
